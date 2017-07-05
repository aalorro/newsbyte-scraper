server "40.117.91.189", port: 22, roles: [:app], :primary => true, user: 'deployer'
set :application => "dev-newsbyte-scrapper"
set :branch, "staging"
set :deploy_to, "/newsbyte_dev"