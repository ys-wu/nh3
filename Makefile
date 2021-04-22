readme:
	pandoc README.md | lynx -stdin

restart-work:
	sudo systemctl restart nh3worker.service
