angular.module("cam", ["ui.router", "ui.bootstrap",  "angular-loading-bar", "ui.select"])


    .run(["$rootScope", "$state", "$stateParams", "$http", "Session", function($rootScope, $state, $stateParams, $http, Session) {
        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        $rootScope.Session = Session;
        $http.get("api/user").then(function(response) {Session.set(response.data);});
    }])


    .config(["$urlRouterProvider", "$stateProvider", "$httpProvider", function($urlRouterProvider, $stateProvider, $httpProvider) {
        $urlRouterProvider.otherwise("/pacientes/ultimos");
        $stateProvider
            .state("patients-last", {
                url: "/pacientes/ultimos",
                templateUrl: "templates/patients-last.html",
                controller: "PatientsLastController"
            })
            .state("patient-new", {
                url: "/paciente/nuevo",
                templateUrl: "templates/patient-profile.html",
                controller: "PatientProfileController"
            })
            .state("patient-view", {
                abstract: true,
                url: "/paciente/{id:int}",
                templateUrl: "templates/patient-view.html",
                controller: "PatientViewController"
            })
            .state('patient-view.summary', {
              url: "",
              templateUrl: "templates/patient-view.summary.html",
              controller: "PatientViewSummaryController"
            })
            .state('patient-view.chronology', {
              url: "/cronologia",
              templateUrl: "templates/patient-view.chronology.html",
              controller: "PatientViewChronologyController"
            })
            .state("patient-edit", {
                url: "/paciente/{id:int}/modificar",
                templateUrl: "templates/patient-profile.html",
                controller: "PatientProfileController"
            });
        $httpProvider.interceptors.push("authorizationInterceptorService");
    }])


    .filter("joinByProp", function() {
        return function(input, property, separator) {
            return !!input? input.map(function(o){ return o[property]; }).join(separator): "";
        };
    })


    .filter("age", function() {
        return function (birthdate) {
            var now = new Date();
            var years = now.getFullYear() - birthdate.getFullYear() - 1;
            if (now.getMonth() > birthdate.getMonth() || (now.getMonth() == birthdate.getMonth() && now.getDate() >= birthdate.getDate())) {
                years += 1;
            }
            return Math.max(0, years);
        };
    })


    .filter("asDate", function() {
        return function(datestring) {
            if (!datestring) {
                return null;
            } else if (datestring.endsWith("Z")) {
                return new Date(datestring);
            } else {
                var ymd = datestring.split("-");
                return new Date(parseInt(ymd[0]), parseInt(ymd[1]) - 1, parseInt(ymd[2]));
            }
        };
    })


    .factory("authorizationInterceptorService", ["$q", "$rootScope", function($q, $rootScope) {
        return {
            responseError: function(rejection) {
                if (rejection.status === 403) {
                    $rootScope.$state.go("patients-last");
                }
                return $q.reject(rejection);
            }
        };
    }])


    .service("Session", function() {
        this.ROLE_ADVISOR = "advisor";
        this.ROLE_SECRETARY = "secretary";
        this.ROLE_SYSTEM_ADMINISTRATOR = "system administrator";
        this.set = function(obj) {angular.extend(this, obj);}
        this.hasRole = function(role) {return !!this.roles && this.roles.indexOf(role) >= 0;}
    })


    .controller("AppController", ["$scope", function($scope) {
        $scope.patientLinks = [];
        $scope.addPatientLink = function(id, name) {
            if (!$scope.patientLinks.some(function(p) {return p.id === id;})) {
                $scope.patientLinks.push({id: id, name: name});
            }
        }
        $scope.removePatientLink = function(num) {
            var removed = $scope.patientLinks.splice(num, 1)[0];
            if ($scope.isPatientLinkActive(removed.id)) {
                $scope.$state.go("patients-last");
            }
        }
        $scope.isPatientLinkActive = function(id) {
            return $scope.$state.includes("patient-view", {id: id});
        }
    }])


    .controller("PatientsLastController", ["$scope", "$http", function($scope, $http) {
        $scope.patients = [];
        $http.get("api/patients/last").then(function(response) {$scope.patients = response.data;});
    }])


    .controller("PatientProfileController", ["$scope", "$http", "$filter", function($scope, $http, $filter) {
        var url = "api/patient";
        $scope.patient = {};
        $scope.child = {};
        $scope.isAdvisorEditable = true;
        $scope.isCoadvisorsEditable = true;
        if ($scope.$stateParams.id) {
            url += "/" + $scope.$stateParams.id;
            $scope.isAdvisorEditable = false;
            $scope.isCoadvisorsEditable = false;
            $http.get(url).then(function(response) {
                var patient = response.data;
                // UI Bootstrap Datepicker requires a Date as model
                patient.birthdate = $filter("asDate")(patient.birthdate);
                // Hack to use ui-select allowing duplicated values
                angular.forEach(patient.children, function(value, key) {value.id = key;});
                $scope.patient = patient;
            });
        }

        $scope.advisors = [];
        $http.get("api/users/advisors").then(function(response) {$scope.advisors = response.data;});

        $scope.processing = false;
        $scope.birthdatePicker = {
            visibility: {},
            options: {startingDay: 1, showWeeks: false, minDate: new Date(1900, 0, 1), maxDate: new Date()}
        };
        $scope.errors = {};

        $scope.addChild = function() {
            if (!$scope.child.name || ($scope.child.known_age && isNaN(parseInt($scope.child.known_age)))) {
                return;
            }

            var child = angular.merge({}, $scope.child);
            child.id = Math.random();
            child.known_age = parseInt(child.known_age);
            if (child.birthdate) {
                child.age = $filter("age")(child.birthdate);
                child.birthdate = $filter("date")(child.birthdate, "yyyy-MM-dd");
            } else {
                child.age = child.known_age;
            }

            if (!$scope.patient.children) {
                $scope.patient.children = [child]
            } else {
                $scope.patient.children.push(child);
            }
            $scope.child = {};
        }

        $scope.editAdvisor = function() {
            $scope.patient.advisor = null;
            $scope.isAdvisorEditable = true;
        }

        $scope.editCoadvisors = function() {
            $scope.patient.coadvisors = [];
            $scope.isCoadvisorsEditable = true;
            $scope.$broadcast("focusCoadvisors");
        }

        $scope.cancel = function() {
            if ($scope.$stateParams.id) {
                $scope.$state.go("patient-view.summary", {id: $scope.$stateParams.id});
            } else {
                $scope.$state.go("patients-last");
            }
        }

        $scope.save = function() {
            $scope.processing = true;
            var patient = angular.merge({}, $scope.patient);
            patient.birthdate = $filter("date")(patient.birthdate, "yyyy-MM-dd");
            $http.post(url, patient).then(function(response) {
                $scope.errors = {};
                $scope.processing = false;
                $scope.$state.go("patient-view.summary", response.data);
            }, function(response) {
                $scope.errors = response.data;
                $scope.processing = false;
            });
        }
    }])


    .controller("PatientViewController", ["$scope", "$http", function($scope, $http) {
        $scope.tabs = {
            summary: $scope.$state.is("patient-view.summary"),
            chronology: $scope.$state.is("patient-view.chronology")
        };
        $http.get("api/patient/" + $scope.$stateParams.id).then(function(response) {
            var patient = $scope.patient = response.data;
            var name = patient.surname? patient.firstname + " " + patient.surname: patient.firstname;
            $scope.$parent.addPatientLink(patient.id, name);
        });
    }])


    .controller("PatientViewSummaryController", ["$scope", function($scope) {
    }])


    .controller("PatientViewChronologyController", ["$scope", function($scope) {
    }]);
