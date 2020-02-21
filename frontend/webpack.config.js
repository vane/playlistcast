const webpack = require('webpack');
const Html = require('html-webpack-plugin');
const Copy = require('copy-webpack-plugin');


module.exports = {
  mode: 'development',
  entry: './src/index.jsx',
  output: {
    path: __dirname + '/build',
    filename: 'index.[hash].js',
    library: 'Playlistcast',
    libraryTarget: 'umd',
    publicPath: '/static/'
  },
  devServer: {
    contentBase: __dirname + '/build',
    compress: false,
    port: 9000,
  },
  module: {
    rules: [
      {
        test: /\.m?(js|jsx)$/,
        exclude: /(node_modules)/,
        use: ['babel-loader', 'eslint-loader'],
      }
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
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
