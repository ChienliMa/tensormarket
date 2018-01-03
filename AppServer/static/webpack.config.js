const webpack = require('webpack');
const config = {
    entry:  __dirname + '/js/index.jsx',
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    module: {
      rules: [
        {
          test: /\.jsx?/,
          exclude: /node_modules/,
          use: 'babel-loader'
        }
      ],
      loaders:[
        {
          test: /\.(js|jsx)$/,
          exclude:"/node_modules/",
          loader: 'babel-loader' ,
          query: {
            presets: ['es2015','react','stage-1'],
            plugins: ['transform-decorators-legacy','transform-decorators']
          }
        }
      ]
    }
};
module.exports = config;