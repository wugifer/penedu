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

requirejs(['app/config'],
    function (config) {

        angular

            .module('mainApp', ['ui.router'])

            .config(config.transition)

            .run(config.location)

            .config(config.index)
        ;

        angular.bootstrap(document, ['mainApp']);
    }
);
