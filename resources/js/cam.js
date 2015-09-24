angular.module("cam", ["ui.router", "ui.bootstrap"])
    .run(["$rootScope", "$state", "$stateParams", "$http", "Session", function($rootScope, $state, $stateParams, $http, Session) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        $http.get("/api/user").then(function(response) {Session.set(response.data);});
    }])
    .config(["$locationProvider", "$urlRouterProvider", "$stateProvider", function($locationProvider, $urlRouterProvider, $stateProvider) {
        $urlRouterProvider.otherwise("/pacientes/ultimos");
        $stateProvider
            .state("patients-last", {
                url: "/pacientes/ultimos",
                templateUrl: "templates/patients-last.html"
            })
            .state("patient-new", {
                url: "/paciente/nuevo",
                templateUrl: "templates/patient-new.html"
            });
    }])
    .service("Session", function() {
        this.ROLE_ADVISOR = "advisor";
        this.user = null;
        this.roles = [];
        this.set = function(obj) {
            this.user = obj.user;
            this.roles = obj.roles;
        }
        this.hasRole = function(role) {return this.roles.indexOf(role) >= 0;}
    })
    .controller("PatientsLastController", ["$scope", "$http", function($scope, $http) {
        $scope.patients = [];
        $http.get("/api/patients/last").then(function(response) {$scope.patients = response.data;});
    }])
    .controller("PatientNewController", ["$scope", "$http", function($scope, $http) {
        $scope.patient = {
            firstname: null,
            middlename: null,
            surname: null,
            birthdate: null,
            nationality: null
        };
        $scope.birthdatePicker = {
            isVisible: false,
            minDate: new Date(1900, 1, 1),
            maxDate: new Date()
        };
        $scope.save = function() {
            $http.post("/api/patient", $scope.patient).then(function(response) {});
        }
    }]);
