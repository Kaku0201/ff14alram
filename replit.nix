{ pkgs }: {
  deps = [
    pkgs.zip
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.pytz
    pkgs.python311Packages.flask
    pkgs.python311Packages.apscheduler
    pkgs.python311Packages.discordpy
  ];
}
