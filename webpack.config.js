// webpack.config.js
module.exports = {
    module: {
      rules: [
        {
          test: /\.jsonl$/i,
          type: 'asset/source'
        },
      ],
    },
  };