server "40.117.91.189", port: 22, roles: [:app], :primary => true, user: 'deployer'
set :application => "newsbyte-scrapper"
set :branch, "master"
set :deploy_to, "/newsbyte"
