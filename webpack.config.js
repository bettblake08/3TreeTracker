const path = require("path"),
    webpack = require("webpack"),
    MiniCssExtractPlugin = require("mini-css-extract-plugin"),
    ManifestRevisionPlugin = require("manifest-revision-webpack-plugin"),
    WebpackMd5Hash = require('webpack-md5-hash');

var root = "./resources/assets";

var jsRoot = `${root}/js`;
var scssRoot = `${root}/scss`;
var pluginRoot = `${root}/plugins`;

var main = {
    scss: `${scssRoot}/pages/main`,
    js: `${jsRoot}/pages/main`
}

var admin = {
    scss: `${scssRoot}/pages/admin`,
    js: `${jsRoot}/pages/admin`
}

var entries = {
    main_css: `${scssRoot}/main.scss`,

    main_home_css: `${main.scss}/home.scss`,

    main_header_js: `${main.js}/header.jsx`,
    main_footer_js: `${main.js}/footer.jsx`,
    main_home_js: `${main.js}/home.jsx`,
    
    admin_css: `${scssRoot}/admin.scss`,
    
    admin_login_css: `${admin.scss}/login.scss`,
    admin_repo_css: `${admin.scss}/repo.scss`,
    admin_accounts_css: `${admin.scss}/accounts.scss`,
    admin_products_css: `${admin.scss}/products.scss`,

    admin_header_js: `${admin.js}/header.jsx`,
    admin_login_js: `${admin.js}/login.jsx`,
    admin_repo_js: `${admin.js}/repo.jsx`,
    admin_products_js: `${admin.js}/products.jsx`,
    admin_accounts_js: `${admin.js}/accounts.jsx`
}

const config = {
    entry: entries,
    output: {
        path: path.resolve(__dirname, 'public/assets'),
        publicPath: "http://127.0.0.1:5000/assets/",
        filename: "[name].[chunkhash].js",
        chunkFilename: "[id].[chunkhash].chunk"
    },
    resolve: {
        extensions: ['.js', '.jsx', '.scss']
    },
    module: {
        rules: [{
                test: /\.(jsx|js)?$/,
                exclude: [/node_modules/],
                use: 'babel-loader'
            },
            {
                test: /\.css$/,
                use: ['style-loader', MiniCssExtractPlugin.loader, 'css-loader']
            },
            {
                test: /\.scss$/,
                use: ['style-loader', MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader']
            },
            {
                test: /\.(jpe?g|png|gif|woff|woff2|eot|ttf|svg)(\?[a-z0-9=.]+)?$/,
                use: ['file-loader']
            }
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].[contenthash].css',
        }),
        new ManifestRevisionPlugin("./manifest.json", {
            rootAssetPath: root
        }),
        new WebpackMd5Hash()
    ]
};

module.exports = config;