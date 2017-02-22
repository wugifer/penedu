define([], function () {

    // 装饰 transitionTo，提前加载需要的模块
    var transitionConfig = function ($provide) {
        // 状态改变前的 hook，用于加载需要的模块
        $provide.decorator('$state', function ($delegate, $stateParams) {
            var state = {};
            angular.copy($delegate, state);
            $delegate.transitionTo = function (to, param, option) {
                // console.log(to, param, option, $delegate);
                if (to.self) {
                    // 不知道什么时候触发，F5刷新页面有时会触发，不总是
                    // to.self 与 $stateProvider.state 的参数相同，貌似此时不需要 decorator
                    state.transitionTo(to, param, option);
                } else {
                    // 点击链接/$state.go()触发，约定：状态规则为 模块名_xxx.other-part
                    tokens = to.split(/[_.]/);
                    if (tokens.length >= 2 && tokens[0] == 'main') {
                        //             // load
                        //             $ocLazyLoad.load(tokens[1])
                        //                 .then(function () {
                        //                     state.transitionTo(to, param, option);
                        //                 }, function () {
                        //                     console.log('load module ' + tokens[1] + ' error!');
                        //                 });
                    } else {
                        //             state.transitionTo(to, param, option);
                    }
                }
            };
            return $delegate;
        });
    };

    // 监听 $locationChangeStart，提前加载需要的模块
    var locationRun = function ($rootScope, $location, $urlRouter) {
        $rootScope.$on('$locationChangeStart', function () {
            // 约定：路径规则为 /模块名/xxx/other-part
            if (!$location.path()) {
                //         $location.path('/');
            }
            // console.log($location.path());
            tokens = $location.path().split('/');
            if (tokens.length >= 3 && tokens[1].length > 1) {
                //         // load
                //         $ocLazyLoad.load(tokens[1])
                //             .then(function () {
                //                     $urlRouter.sync();
                //                     $urlRouter.listen();
                //                 },
                //                 function (err) {
                //                     console.log('load module ' + tokens[1] + ' error!');
                //                     console.log(err);
                //                 });
            }
        });
    };

    // 首页、重定向
    var indexConfig = function ($stateProvider, $urlRouterProvider) {
        $urlRouterProvider
            .when('', '/');

        $stateProvider
            .state('main', {    // 首页父框架
                url: '/',
                views: {
                    user: {
                        templateUrl: 'user.html'
                    },
                    menu: {
                        templateUrl: 'menu.html',
                        controller: function ($scope) {
                        }
                    },
                    header: {
                        template: '<div ui-view="header"></div>'
                    },
                    content: {
                        template: '<div ui-view="content"></div>'
                    }
                }
            });
    };

    return {
        'transition': transitionConfig,
        'location': locationRun,
        'index': indexConfig
    };
});
