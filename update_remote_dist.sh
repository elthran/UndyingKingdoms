ssh undyingkingdoms@ssh.pythonanywhere.com "rm -r ~/UndyingKingdoms/undyingkingdoms/static/dist && exit"
scp -r undyingkingdoms/static/dist undyingkingdoms@ssh.pythonanywhere.com:~/UndyingKingdoms/undyingkingdoms/static

