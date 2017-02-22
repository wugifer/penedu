define(['app/md5', 'app/date'], function (md5, date) {

    var loginController = function ($scope, $http) {
        $scope.user = {
            login: '',
            pass: '',
            hash: ''
        };

        // 计算密码
        var makePassword = function () {
            var now = date.format(new Date(), 'yyyy-mm-dd HH:MM');
            var hash = md5($scope.user.pass);
            $scope.user.hash = md5(now + hash);
        };

        // 登录
        $scope.loginClick = function () {
            makePassword();
            $http({
                method: 'POST',
                url: '/user/login',
                data: {
                    login: $scope.user.login,
                    hash: $scope.user.hash
                },
                responseType: 'json'
            }).success(function (data) {
                location = '/';
            });
        };
    };

    loginController.$inject = ['$scope', '$http'];

    return loginController;
});
