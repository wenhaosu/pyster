set -x

python3 -m pyster \
  --project_path ../public_repo/codetiming \
  --module_name codetiming._timer \
  --timeout 5 \
  --coverage 100