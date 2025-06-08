
const path = require('path');
const webpack = require('webpack');
const dotenv = require('dotenv');

// Call dotenv and it will return an Object with a parsed key 
const env = dotenv.config().parsed || {};

// Create a new webpack.DefinePlugin that will inject environment variables
const envKeys = Object.keys(env).reduce((prev, next) => {
  prev[`process.env.${next}`] = JSON.stringify(env[next]);
  return prev;
}, {});

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'main.js',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
          },
        },
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          'style-loader',
          'css-loader',
          'sass-loader',
        ],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  plugins: [
    new webpack.DefinePlugin(envKeys)
  ],
  devServer: {
    static: path.join(__dirname, 'public'),
    port: 8080,
    hot: true,
  },
};