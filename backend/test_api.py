"""
API contract tests.

These run with no MongoDB and no OPENAI_API_KEY, which is exactly how CI and a
fresh clone are configured. That is deliberate: every endpoint is supposed to
degrade to its deterministic path rather than fail, and these tests are what
prove it.
"""

import os

import pytest
from fastapi.testclient import TestClient

# Must be cleared before server is imported, so the module-level key read in
# ai_client sees an unconfigured environment.
for _k in ("OPENAI_API_KEY", "GROQ_API_KEY"):
    os.environ.pop(_k, None)

from server import app  # noqa: E402

client = TestClient(app)


# --------------------------------------------------------------- basics

def test_root_reports_running():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "running"


def test_health_reports_dependency_state():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "healthy"
    # Without a key the service must say so rather than pretend AI is live.
    assert body["dependencies"]["ai"]["ok"] is False
    assert body["dependencies"]["ai"]["provider"] in {"Groq", "OpenAI"}
    assert body["careers_available"] > 0
    assert "ai_metrics" in body


# --------------------------------------------------------------- careers

def test_careers_returns_catalogue():
    r = client.get("/careers")
    assert r.status_code == 200
    careers = r.json()
    assert len(careers) >= 20
    assert {"id", "title", "category", "required_skills"} <= set(careers[0])


def test_career_detail_round_trips():
    r = client.get("/careers/frontend-developer")
    assert r.status_code == 200
    assert r.json()["title"] == "Frontend Developer"


def test_unknown_career_is_404_not_500():
    assert client.get("/careers/not-a-real-career").status_code == 404


@pytest.mark.parametrize("query", ["data", "cyber", "python"])
def test_search_finds_matches(query):
    r = client.get("/careers/search", params={"q": query})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.parametrize("query", ["C++", "((", "a|b", "*", ".*"])
def test_search_survives_regex_metacharacters(query):
    """A raw query string must never be compiled as a regex."""
    r = client.get("/careers/search", params={"q": query})
    assert r.status_code == 200


def test_roadmap_has_ordered_steps():
    r = client.get("/careers/frontend-developer/roadmap")
    assert r.status_code == 200
    body = r.json()
    assert body["career"] == "Frontend Developer"
    assert len(body["roadmap"]) > 0


# -------------------------------------------------------- taxonomy

def test_categories_counts_match_careers():
    r = client.get("/categories")
    assert r.status_code == 200
    body = r.json()
    assert body["total_categories"] > 0
    total = sum(c["career_count"] for c in body["categories"])
    assert total == len(client.get("/careers").json())


def test_skills_ranked_by_demand():
    r = client.get("/skills", params={"limit": 10})
    assert r.status_code == 200
    skills = r.json()["skills"]
    assert len(skills) == 10
    scores = [s["demand_score"] for s in skills]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.parametrize("limit", [0, -1, 501, 10000])
def test_skills_rejects_out_of_range_limit(limit):
    assert client.get("/skills", params={"limit": limit}).status_code == 422


# -------------------------------------------------- recommendations

def test_recommendations_are_sorted_and_explained():
    r = client.post(
        "/recommendations",
        json={
            "skills": ["Python", "SQL", "Machine Learning"],
            "interests": ["AI"],
            "education_level": "Bachelors",
            "experience_years": 2,
            "goals": "Become an ML engineer",
        },
    )
    assert r.status_code == 200
    recs = r.json()["recommendations"]
    assert len(recs) > 0
    scores = [x["match_score"] for x in recs]
    assert scores == sorted(scores, reverse=True)
    # With no API key every explanation comes from the rule-based path.
    assert all(x["reasoning"] for x in recs)


def test_recommendations_handle_empty_profile():
    """An empty profile must still return something, not a 500."""
    r = client.post("/recommendations", json={})
    assert r.status_code == 200
    assert len(r.json()["recommendations"]) > 0


# ------------------------------------------------------------ skill gap

def test_skill_gap_splits_known_and_missing():
    r = client.post(
        "/skill-gap",
        json={
            "career_id": "frontend-developer",
            "skills": ["HTML", "CSS", "JavaScript"],
            "experience_years": 1,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert set(body["skills_matched"]) == {"HTML", "CSS", "JavaScript"}
    assert "React" in body["skills_missing"]
    assert 0 <= body["coverage"] <= 1
    # Every missing skill must appear exactly once in the priority order.
    assert sorted(body["priority_order"]) == sorted(body["skills_missing"])


def test_skill_gap_is_case_insensitive():
    r = client.post(
        "/skill-gap",
        json={"career_id": "frontend-developer", "skills": ["html", "CSS"]},
    )
    assert r.status_code == 200
    assert set(r.json()["skills_matched"]) == {"HTML", "CSS"}


def test_skill_gap_unknown_career_is_404():
    r = client.post("/skill-gap", json={"career_id": "nope", "skills": []})
    assert r.status_code == 404


# ------------------------------------------------------------- profiles

def test_profile_save_and_fetch_round_trip():
    created = client.post(
        "/profiles",
        json={"skills": ["Python"], "interests": ["AI"], "experience_years": 3},
    )
    assert created.status_code == 201
    profile_id = created.json()["profile_id"]

    fetched = client.get(f"/profiles/{profile_id}")
    assert fetched.status_code == 200
    body = fetched.json()
    assert body["profile"]["skills"] == ["Python"]
    assert len(body["recommendations"]) > 0


def test_unknown_profile_is_404():
    assert client.get("/profiles/deadbeef").status_code == 404


# ------------------------------------------------- schema validation layer

def test_schema_validator_rejects_wrong_shape():
    """The guard that turns a malformed generation into a retry."""
    from ai_client import SchemaValidationError, _validate
    from schemas import REASONING_SCHEMA

    _validate({"reasoning": "x" * 50}, REASONING_SCHEMA)  # valid

    with pytest.raises(SchemaValidationError):
        _validate({"wrong_key": "value"}, REASONING_SCHEMA)
    with pytest.raises(SchemaValidationError):
        _validate({"reasoning": "too short"}, REASONING_SCHEMA)


@pytest.mark.anyio
async def test_generate_validated_raises_without_key():
    from ai_client import AIUnavailable, generate_validated
    from schemas import REASONING_SCHEMA

    with pytest.raises(AIUnavailable):
        await generate_validated(
            system="s", user="u", schema=REASONING_SCHEMA
        )


@pytest.fixture
def anyio_backend():
    return "asyncio"
