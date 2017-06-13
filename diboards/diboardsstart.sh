now=$(date)
me="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"
echo "Restart from $me"
echo "$now"
echo "-------------------------------------------------------------"
gunicorn -w 2 -b 127.0.0.1:5000 diboards:app &
echo "-------------------------------------------------------------"
/usr/sbin/nginx -g "daemon off;"