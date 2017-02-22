requirejs.config({
    // 缺省路径
    baseUrl: '/static/js/lib',

    // 例外路径，不含 .js 后缀
    paths: {
        app: '/static/js/app'
    },

    // 其它
    shim: {}
});

requirejs(['app/login.controller'],
    function (loginController) {

        angular

            .module('loginApp', [])

            .controller('loginController', loginController);

        angular.bootstrap(document, ['loginApp']);
    }
);
