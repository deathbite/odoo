# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

import urllib
from tools.safe_eval import safe_eval
import pooler
import config
import release

def send_ping(cr, uid):
    pool = pooler.get_pool(cr.dbname)
    
    dbuuid = pool.get('ir.config_parameter').get_param(cr, uid, 'database.uuid')
    nbr_users = pool.get("res.users").search(cr, uid, [], count=True)
    contractosv = pool.get('maintenance.contract')
    contracts = contractosv.browse(cr, uid, contractosv.search(cr, uid, []))
    msg = {
        "dbuuid": dbuuid,
        "nbr_users": nbr_users,
        "dbname": cr.dbname,
        "version": release.version,
        "contracts": [c.name for c in contracts],
    }
    
    uo = urllib.urlopen(config.config.get("ping_url"),  urllib.urlencode({'arg0': msg,}))
    try:
        submit_result = uo.read()
    finally:
        uo.close()
    
    result = safe_eval(submit_result)
    
    return result



