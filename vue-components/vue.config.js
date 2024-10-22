const path = require('path');
const DST_PATH = '../trame_gwc/module/serve';

module.exports = {
    lintOnSave: false,
    outputDir: path.resolve(__dirname, DST_PATH),
    publicPath: './'
};