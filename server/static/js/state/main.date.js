define(['app/global'], function (g) {
    g.register.state
        .state('main.date', {
            'url': '^/date',
            'views': {
                'content': {
                    'template': '{{ hello }}',
                    'controller': function ($scope) {
                        $scope.hello = 'world';
                    }
                }
            }
        })
    ;
});
