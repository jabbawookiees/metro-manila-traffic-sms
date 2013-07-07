#!/bin/bash
dir=$(dirname $0)
vendor=$dir/vendor_modules
puppet apply $dir/traffic.pp --modulepath=$vendor | tee $dir/puppet.log
