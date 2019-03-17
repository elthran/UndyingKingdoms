HOST="undyingkingdoms@ssh.pythonanywhere.com"
ssh $HOST '
rm -r ~/UndyingKingdoms/undyingkingdoms/static/dist
exit
'
scp -r << EOF
  undyingkingdoms/static/dist $HOST:~/UndyingKingdoms/undyingkingdoms/static
EOF

