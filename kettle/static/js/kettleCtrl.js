(function() {
angular.module("kettleApp")
.controller("kettleCtrl",function($scope,$http) {
    $scope.model = {
        beer_list: []
    }
    $scope.like_beers = ['samael-s'];
    $scope.dont_beers = ['ipa'];
    $scope.postBeers = postBeers;

    $http.get('/kettle/beer_list').then(
        function(data) {
            $scope.model.beer_list = data.data.result;
            console.log($scope.model.beer_list);
        },
        function () {}
    );


    function postBeers() {
        $http.post('/kettle/crunch',{like_ids:$scope.like_beers,dislike_ids:$scope.dont_beers}).then(
        function (data) { 
            console.log(data);
            alert('<img src="http://http://media.giphy.com/media/rnR8L2AtvBpD2/giphy-tumblr.gif"></img>');
        },
        function () { 
            alert('failed');
        });
    }
});
})()
