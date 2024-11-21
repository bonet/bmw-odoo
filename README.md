To start:
```
docker compose up
```

To connect to Odoo shell:
```
- # make sure that you ran docker compose up
- docker compose exec odoo bash
- odoo shell -d bmw-odoo --db_host postgres --db_port 5432 --db_user odoo --db_password odoo
```

To add a new module:
```
# First, update the module list to make sure Odoo sees your module
env['ir.module.module'].update_list()

# Then install the module
module = env['ir.module.module'].search([('name', '=', 'bmw_crm')])
module.button_immediate_install()

# Don't forget to commit the changes
env.cr.commit()
```

To upgrade a module:
```
# 1. Find the module to upgrade
module = env['ir.module.module'].search([('state', '=', 'to upgrade')])
print(f"Module to upgrade: {module.name}")  # Verify it's the right one

# 2. Method 1 - Direct upgrade:
module.button_immediate_upgrade()
env.cr.commit()
```
