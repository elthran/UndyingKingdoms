HOST="undyingkingdoms@ssh.pythonanywhere.com"
ssh $HOST '
rm -r ~/UndyingKingdoms/undyingkingdoms/static/dist
rm -r ~/UndyingKingdoms/undyingkingdoms/templates/dist
exit
'
scp -r << EOF
  undyingkingdoms/static/dist $HOST:~/UndyingKingdoms/undyingkingdoms/static
  undyingkingdoms/templates/dist $HOST:~/UndyingKingdoms/undyingkingdoms/templates
EOF

