$env = 'development'
if $env == 'development' {
  $config_dir = '/home/user/corgi/puppet/configs'
  $machine_user = 'user'
  $machine_group = 'user'
} elsif $env == 'production' {
  $config_dir = '/home/user/corgi/puppet/configs'
  $machine_user = 'user'
  $machine_group = 'user'
}

# Ensure 'apt-get update' is run before trying to install any packages.
# TODO: find a way to make this run only if there is something to
# install or upgrade; see http://projects.puppetlabs.com/issues/3986.
exec {'/usr/bin/apt-get update': } -> Package <| provider == 'apt' |>

class kannel {
  package {'usb-modeswitch': }
  package {'kannel': }
  service {'kannel':
    ensure => running
  }
  file {'/etc/kannel/kannel.conf':
    ensure => present,
    source => "${config_dir}/kannel/kannel.conf",
    owner => 'root',
    group => 'root',
    require => Package['kannel'],
    before => Service['kannel'],
    notify => Service['kannel'],
  }
  file {'/var/spool/kannel':
    ensure => directory,
    owner => 'kannel',
    require => Package['kannel'],
    before => Service['kannel'],
  }
  file {'/etc/default/kannel':
    ensure => present,
    source => "${config_dir}/default/kannel",
    owner => 'root',
    group => 'root',
    require => Package['kannel'],
    before => Service['kannel'],
    notify => Service['kannel'],
  }
  file {'/etc/udev/rules.d/90-kannel-gsm.rules':
    ensure => present,
    source => "${config_dir}/udev/rules.d/90-kannel-gsm.rules",
    owner => 'root',
    group => 'root',
    before => Service['kannel'],
  }
}

class python {
  package {'python2.7': }
  package {'python-dev': }
  package {'python-pip':
    require => [Package['python2.7']],
  }
  package {'redis-server': }
  package {'redis':
    provider => 'pip',
    require => [Package['redis-server']],
  }
  package {'rq':
    provider => 'pip',
    require => [Package['python-pip'], Package['redis']],
  }
  package {'flask':
    provider => 'pip',
    require => [Package['python-pip']],
  }
}

class services {
  file {'/etc/init/transit-backend.conf':
    content => template("$config_dir/init/transit-backend.conf"),
    owner => 'root',
    group => 'root'
  }
  service {'transit-backend':
    ensure => running,
    require => [File['/etc/init/transit-backend.conf'], Class['backend'] ]
  }
  file {'/etc/init/transit-queue.conf':
    content => template("$config_dir/init/transit-queue.conf"),
    owner => 'root',
    group => 'root'
  }
  service {'transit-queue':
    ensure => running,
    require => [File['/etc/init/transit-queue.conf'], Class['backend'] ]
  }
}

class utils{
  package {'curl': }
  package {'vim': }
}

case $env {
  'development': {
    class {'kannel': }
    class {'python': }
    class {'services': }
    class {'utils': }
  }
  'production': {
    class {'kannel': }
    class {'python': }
    class {'services': }
  }
}
