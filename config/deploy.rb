set :stages, %w(production staging)
set :default_stage, "production"
set :repo_url, "git@gitlab.com:incubixtech/newsbyte-scrapy.git"
set :scm, :git

set :user, "deployer"
set :pty, true

set :ssh_options, { :auth_methods => ["publickey"], forward_agent: true, user: fetch(:user), :keys => [
        "C:\\Users\\IncubixTech\\Workspace\\_keys\\newsbyte\\newsbyte.pem"
    ]
}

set :keep_releases, 3

# set :linked_dirs, %w{storage public/images public/fonts public/font-awesome public/css public/js}

namespace :git do
    desc "Make sure local git is in sync with remote."
    task :check_revision do
        on roles(:app) do
            unless `git rev-parse HEAD` == `git rev-parse origin/master`
                puts "WARNING: HEAD is not the same as origin/master"
                puts "Run `git push` to sync changes."
                exit
            end
        end
    end
end

namespace :filesystem do
    desc "Change deploy folder's ownership to psacln"
    task :ownership do
        on roles(:app), in: :sequence, wait: 5 do
            within release_path do
                execute :chown, "-R", "deployer:psacln", "#{current_path}/*"
                execute :chown, "-R", "deployer:psacln", "env/*"
            end
        end
    end
    task :permissions do
        on roles(:app), in: :sequence, wait: 5 do
            within release_path do
                execute :chmod, "775 -R", "#{current_path}/*"
                execute :chmod, "775 -R", "env/*"
            end
        end
    end
end

namespace :deploy do
    # after :published, "git:check_revision"
    after :published, "filesystem:ownership"
end