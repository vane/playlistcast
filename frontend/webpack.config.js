const webpack = require('webpack');
const Html = require('html-webpack-plugin');
const Copy = require('copy-webpack-plugin');

const mode = 'development'

module.exports = {
  mode,
  entry: './src/index.jsx',
  output: {
    path: __dirname + '/build',
    filename: mode === 'production' ? 'index.[hash].js' : 'index.js',
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
      },
      {
        test: /\.(less|css)$/,
        use: ['style-loader', {
          loader: 'css-loader',
          options: {
            sourceMap: true
          }
        }, 'less-loader']
      }
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  plugins: [
    new Html({
      template: mode === 'production' ? 'index.html' : 'index.debug.html',
    }),
    new Copy([
      {from: 'assets'},
    ]),
  ]
}
