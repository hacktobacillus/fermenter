(function() {
angular.module("kettleApp")
.controller("kettleCtrl",function($scope,$http) {
    $scope.model = {
        beer_list: []
    }

    

    $scope.like_beers = [];
    $scope.dislike_beers = [];
    $scope.postBeers = postBeers;
    $scope.downVoteBeer = downVoteBeer;
    $scope.upVoteBeer = upVoteBeer;


    $http.get('/kettle/beer_list').then(
        function(data) {
            $scope.model.beer_list = data.data.result;
            console.log($scope.model.beer_list);
        },
        function () {}
    );


    function upVoteBeer(beer) {
        // return if this beer has been voted on.
        if (beer.voted_on) {
            return;
        }
        var beer_exists = false;
        for (var i in $scope.like_beers) {
            var bid  = $scope.like_beers[i];
            if (beer.id == bid) {
                beer_exists = true;
                break
            }
        }
        if (!beer_exists) {
            $scope.like_beers.push(beer.id);
        }

        // Make sure it's not in dislike beers.
        for (var i in $scope.dislike_beers) {
            var bid  = $scope.dislike_beers[i];
            // remove it if present
            if (beer.id == bid) {
                $scope.dislike_beers.splice(i,1);
                beer.voted_on = false;
                return;
            }
        }
        beer.voted_on = true;
        console.log([$scope.like_beers,$scope.dislike_beers]);
    }

    function downVoteBeer(beer) {
        console.log(beer);
        // return if this beer has been voted on.
        if (beer.voted_on) {
            return;
        }
        var beer_exists = false;
        for (var i in $scope.dislike_beers) {
            var bid  = $scope.dislike_beers[i];
            if (beer.id == bid) {
                beer_exists = true;
                break
            }
        }
        if (!beer_exists) {
            $scope.dislike_beers.push(beer.id);
        }

        // Make sure it's not in like beers.
        for (var i in $scope.like_beers) {
            var bid  = $scope.like_beers[i];
            // remove it if present
            if (beer.id = bid) {
                $scope.like_beers.splice(i,1);
                beer.voted_on = false;
                return;
            }
        }
        beer.voted_on = true;
        console.log([$scope.like_beers,$scope.dislike_beers]);
     }


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
