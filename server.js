// Webpack dev server
import webpack from 'webpack';
import WebpackDevServer from 'webpack-dev-server';

import config from './webpack.local.config';

new WebpackDevServer(
  {
    // publicPath: config.output.publicPath,
    port: 3000,
    hot: true,
    // inline: true,
    historyApiFallback: true,
    headers: { 'Access-Control-Allow-Origin': '*' },
  },
  webpack(config)
).startCallback((err) => {
  if (err) {
    console.log(err);
  }

  console.log('Front-End now running on port 3000!');
});
