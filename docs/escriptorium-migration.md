# eScriptorium Migration: Staging → Production

## Server Info

| | Staging | Production |
|---|---|---|
| Host | `cdh-test-htr1.lib.princeton.edu` | `cdh-htr1.lib.princeton.edu` |
| DB name | `cdh_test_htr` | `cdh_htr` |
| DB user | `cdh_test_htr` | `cdh_htr` |
| DB server | `lib-postgres-staging1.princeton.edu` | `lib-postgres-prod1.princeton.edu` |
| Media files | `/mnt/nfs/cdh/htr/media/` (329GB) | `/mnt/tigerdata/cdh/htr/media/` |
| URL | `https://test-htr.princeton.edu` | `https://htr.cdh.princeton.edu` |

## Completed

### 1. Database dump (2026-04-30)

On staging server (`cdh-test-htr1`):

```bash
mkdir -p /mnt/nfs/cdh/htr/migrate
pg_dump -Fc -U cdh_test_htr -h lib-postgres-staging1.princeton.edu cdh_test_htr \
  > /mnt/nfs/cdh/htr/migrate/escriptorium_staging.dump
```

Result: 1.4GB dump at `/mnt/nfs/cdh/htr/migrate/escriptorium_staging.dump`

Notes:
- DB is on `lib-postgres-staging1`, not `lib-postgres-prod1`
- Root disk `/` was 100% full — used NFS path instead of `~/migrate`
- Enter password at prompt; do not paste it into the command line

### 2. Transfer dump to production (2026-05-01)

`rsync` does not support two remote endpoints. `pulsys` has no SSH private key on staging.
Solution: use `ssh -A` (agent forwarding) to forward your local key to staging, then rsync from there.
The `-A` flag is temporary — the forwarded key is gone when the SSH session ends.

From local machine:
```bash
ssh -A pulsys@cdh-test-htr1.lib.princeton.edu
```

Then on staging:
```bash
rsync -avz --progress \
  /mnt/nfs/cdh/htr/migrate/escriptorium_staging.dump \
  pulsys@cdh-htr1.lib.princeton.edu:/tmp/escriptorium_staging.dump
```

Result: 1.4GB transferred in 13 seconds, file at `/tmp/escriptorium_staging.dump` on `cdh-htr1`

### 3. Created `htr_production` ansible group_vars

- `inventory/group_vars/htr_production/vars.yml` — production variables (DB name, URL, TigerData, etc.)
- `inventory/group_vars/htr_production/vault.yml` — still needed (DB password, Django secret key)

---

## Still To Do

### Before data restore

- [ ] Create `htr_production/vault.yml` with encrypted DB password and Django secret key
- [ ] Update `playbooks/escriptorium.yml` to support production (currently targets `htr_staging` only)
- [ ] Run ansible deploy playbook against production — this will create the `conan` user, create the DB, configure postgres access (`pg_hba.conf`), and mount TigerData

### Data restore (after deploy)

On production server (`cdh-htr1`):

```bash
pg_restore --no-owner \
  -U cdh_htr \
  -h lib-postgres-prod1.princeton.edu \
  -d cdh_htr \
  /tmp/escriptorium_staging.dump
```

Update the site URL in the database:
```bash
psql -U cdh_htr -h lib-postgres-prod1.princeton.edu -d cdh_htr \
  -c "UPDATE django_site SET domain = 'htr.cdh.princeton.edu', name = 'htr.cdh.princeton.edu' WHERE id = 1;"
```

Run Django migrations:
```bash
sudo -u conan /srv/www/escriptorium/app/env/bin/python \
  /srv/www/escriptorium/app/manage.py migrate
```

### Media files (329GB, after TigerData is mounted)

Use `tmux` to avoid losing the transfer if SSH disconnects:
```bash
tmux new -s migrate
```

From staging (with `ssh -A`):
```bash
rsync -avz --progress \
  /mnt/nfs/cdh/htr/media/ \
  conan@cdh-htr1.lib.princeton.edu:/mnt/tigerdata/cdh/htr/media/
```

---

## Switchover Plan

### Before switching

1. Christine tests production instance (target: 2026-05-11)
2. Re-run pg_dump + media rsync on switchover day to capture latest data
3. Notify Ed's team 1-2 weeks in advance (owner: Jeri)

### Lock down staging

To prevent users from writing to the old site after switching:

**Option A: Disable CAS login (recommended)** — netid login stops working; admin username login still works. Redeploy staging after changing ansible vars.

**Option B: Warning banner** — `SHOW_TEST_WARNING` is already supported in `escriptorium_settings.py.j2`. Add a message pointing to the new URL. Does not block login.

**Option C: Both** — show banner first, disable CAS on switchover day.

### After switching

- Confirm production is running correctly
- Decommission or reset old staging instance within 1-2 weeks
