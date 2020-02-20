const webpack = require('webpack');
const Html = require('html-webpack-plugin');
const Copy = require('copy-webpack-plugin');


module.exports = {
  mode: 'development',
  entry: './src/index.js',
  output: {
    path: __dirname + '/build',
    filename: 'index.[hash].js',
    library: 'Armator',
    libraryTarget: 'umd',
    publicPath: '/static/'
  },
  devServer: {
    contentBase: __dirname + '/build',
    compress: false,
    port: 9000
  },
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
        },
      }
    ],
  },
  plugins: [
    new Html({
      template: 'index.html',
    }),
    new Copy([
      {from: 'assets'},
    ]),
  ]
}
