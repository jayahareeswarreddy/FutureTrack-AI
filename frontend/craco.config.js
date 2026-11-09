// CRA 5 pins its own postcss options inline, which stops postcss-loader from
// discovering postcss.config.js. `mode: 'file'` tells craco to hand that file
// back to the loader, so Tailwind and autoprefixer actually run.
module.exports = {
  style: {
    postcss: {
      mode: 'file',
    },
  },
};
