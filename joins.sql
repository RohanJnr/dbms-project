select pack_id, GROUP_CONCAT(CONCAT(users.user_id, " | ", users.first_name)) from user_packs join users on users.user_id=user_packs.user_id group by pack_id;

select pack_id, GROUP_CONCAT(CONCAT(sites.site_id, '|', sites.site_name)) from pack_sites join sites on sites.site_id=pack_sites.site_id group by pack_id;

select travel_packs.pack_id, travel_packs.destination, sites.site_id, sites.site_name, sites.entry_fee from pack_sites join sites on sites.site_id=pack_sites.site_id join travel_packs on travel_packs.pack_id = pack_sites.pack_id;