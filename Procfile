web: gunicorn bechdel.wsgi --chdir backend --limit-request-line 8188 --log-file -
worker: REMAP_SIGTERM=SIGQUIT celery --workdir backend --app=bechdel worker --loglevel=info
beat: REMAP_SIGTERM=SIGQUIT celery --workdir backend --app=bechdel beat -S redbeat.RedBeatScheduler --loglevel=info
