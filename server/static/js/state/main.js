requirejs.config({
    // 缺省路径
    baseUrl: '/static/js/lib',

    // 路径映射
    map: {
        '*': {   // 任意 requirejs 请求者
            'c': 'css.min' // css --> css.min --> /static/js/lib/css.min.js
        }
    },

    // 例外路径，不含 .js 后缀
    paths: {
        css: '/static/css',
        app: '/static/js/app',
        state: '/static/js/state'
    },

    // 全局依赖关系
    shim: {}
});

requirejs(['app/global', 'app/config'],
    function (g, config) {

        app = angular

            .module('mainApp', ['ui.router'])

            .config(config.transition)

            .run(config.location)

            .config(config.index)

            .config(function ($stateProvider) {
                g.register = {
                    state: $stateProvider
                };
            })
        ;

        angular.bootstrap(document, ['mainApp']);

        g.app = app;
    }
);
