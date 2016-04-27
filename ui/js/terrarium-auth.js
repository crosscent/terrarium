var terrariumAuth = angular.module('terrarium.auth', ['ngRoute', 'ngResource']);

terrariumAuth.config(function($routeProvider) {

    $routeProvider.
        when('/login', {
            templateUrl: 'partials/main/login.html',
            controller: 'AuthController'
        }).
        when('/logout', {
            templateUrl: 'partials/main/logout.html',
            controller: 'AuthController'
        })

});

terrariumAuth.config(function($httpProvider){
    // django and angular both support csrf tokens. This tells angular which cookie to add to what header.
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

terrariumAuth.factory('api', function($resource) {
    function add_auth_header(config) {
        // as per HTTP authentication spec, credentials must be encoded in base64.
        return 'Basic ' + btoa(config.data.username + ':' + config.data.password);
    }
       // defining the endpoints. Not we escape url trailing dashes: Angular
       // stripes unescaped trailing slashes. Problem as Django redirects urls
       // not ending in slashes to url that end in slash for SEO reasons,
       // unless we tell Django not to. This is a problem as the POST data
       // cannot be sent with the redirect. So we want Angular not to strip the
       // slashes
       return {
           auth: $resource('/api/account/auth\\/', {}, {
               login: {method: 'POST',
                       headers: {'Authorization': add_auth_header}}, 
               logout: {method: 'DELETE'}
           }),
           user: $resource('/api/account\\/', {}, {
               create: {method: 'POST'}      
           })
       } ;
});

terrariumAuth.controller('AuthController', function($scope, api){
    $scope.getCredentials = function() {
        return {username: $scope.username,
                password: $scope.password};
    };

    $scope.login = function() {
        api.auth.login($scope.getCredentials()).
            $promise.
                then(function(data) {
                    // on good username and password
                    $scope.user = data.username;
                }).
                catch(function(data) {
                    // on incorect username and password
                    alert(data.data.detail);
                })
    };

    $scope.logout = function() {
        api.auth.logout(function() {
            $scope.user = undefined;
        });
    };

    $scope.register = function($event) {
        // prevent login form from firing
        $event.preventDefault();
        // create user and immediately login on success
        api.users.create($scope.getCredentials()).
            $promise.
                then($scope.login).
                catch(function(data) {
                    alert(data.data.username);
                });
    };
});
