requirejs.config({
    // 缺省路径
    baseUrl: '/static/js/lib',

    // 例外路径，不含 .js 后缀
    paths: {
        app: '/static/js/app',
        state: '/static/js/state'
    },

    // 其它
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
