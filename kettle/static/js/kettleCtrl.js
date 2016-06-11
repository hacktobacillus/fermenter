(function() {
angular.module("kettleApp")
.controller("kettleCtrl",function($scope,$http) {

    $scope.like_beers = ['samael-s'];
    $scope.dont_beers = ['ipa'];
    $scope.postBeers = postBeers;

    $http.get('/kettle/beer_list').then(
        function(data) {
            console.log(JSON.parse(data.data));
        },
        function () {}
    );


    function postBeers() {
        $http.post('/kettle/crunch',{like_ids:$scope.like_beers,dislike_ids:$scope.dont_beers}).then(
        function (data) { 
            console.log(data);
            alert('success!');
        },
        function () { 
            alert('failed');
        });
    }
});
})()
