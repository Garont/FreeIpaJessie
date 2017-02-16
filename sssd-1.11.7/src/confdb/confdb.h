/*
   SSSD

   NSS Configuratoin DB

   Copyright (C) Simo Sorce <ssorce@redhat.com>	2008

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef _CONF_DB_H
#define _CONF_DB_H

#include <stdbool.h>
#include "talloc.h"
#include "tevent.h"
#include "ldb.h"
#include "ldb_errors.h"
#include "config.h"

/**
 * @defgroup sss_confdb The ConfDB API
 * The ConfDB is an interface for data providers to
 * access the configuration information provided in
 * the sssd.conf
 * @{
 */

#define CONFDB_FILE "config.ldb"
#define CONFDB_DEFAULT_CONFIG_FILE SSSD_CONF_DIR"/sssd.conf"
#define SSSD_MIN_ID 1
#define SSSD_LOCAL_MINID 1000
#define CONFDB_DEFAULT_SHELL_FALLBACK "/bin/sh"


/* Configuration options */

/* Services */
#define CONFDB_SERVICE_PATH_TMPL "config/%s"
#define CONFDB_SERVICE_COMMAND "command"
#define CONFDB_SERVICE_DEBUG_LEVEL "debug_level"
#define CONFDB_SERVICE_DEBUG_TIMESTAMPS "debug_timestamps"
#define CONFDB_SERVICE_DEBUG_MICROSECONDS "debug_microseconds"
#define CONFDB_SERVICE_DEBUG_TO_FILES "debug_to_files"
#define CONFDB_SERVICE_TIMEOUT "timeout"
#define CONFDB_SERVICE_FORCE_TIMEOUT "force_timeout"
#define CONFDB_SERVICE_RECON_RETRIES "reconnection_retries"
#define CONFDB_SERVICE_FD_LIMIT "fd_limit"
#define CONFDB_SERVICE_ALLOWED_UIDS "allowed_uids"

/* Monitor */
#define CONFDB_MONITOR_CONF_ENTRY "config/sssd"
#define CONFDB_MONITOR_SBUS_TIMEOUT "sbus_timeout"
#define CONFDB_MONITOR_ACTIVE_SERVICES "services"
#define CONFDB_MONITOR_ACTIVE_DOMAINS "domains"
#define CONFDB_MONITOR_TRY_INOTIFY "try_inotify"
#define CONFDB_MONITOR_KRB5_RCACHEDIR "krb5_rcache_dir"
#define CONFDB_MONITOR_DEFAULT_DOMAIN "default_domain_suffix"
#define CONFDB_MONITOR_OVERRIDE_SPACE "override_space"

/* Both monitor and domains */
#define CONFDB_NAME_REGEX   "re_expression"
#define CONFDB_FULL_NAME_FORMAT "full_name_format"
#define CONFDB_DEFAULT_FULL_NAME_FORMAT_INTERNAL  "%1$s@%2$s%3$s"
#define CONFDB_DEFAULT_FULL_NAME_FORMAT           "%1$s@%2$s"

/* Responders */
#define CONFDB_RESPONDER_GET_DOMAINS_TIMEOUT "get_domains_timeout"
#define CONFDB_RESPONDER_CLI_IDLE_TIMEOUT "client_idle_timeout"
#define CONFDB_RESPONDER_CLI_IDLE_DEFAULT_TIMEOUT 60

/* NSS */
#define CONFDB_NSS_CONF_ENTRY "config/nss"
#define CONFDB_NSS_ENUM_CACHE_TIMEOUT "enum_cache_timeout"
#define CONFDB_NSS_ENTRY_CACHE_NOWAIT_PERCENTAGE "entry_cache_nowait_percentage"
#define CONFDB_NSS_ENTRY_NEG_TIMEOUT "entry_negative_timeout"
#define CONFDB_NSS_FILTER_USERS_IN_GROUPS "filter_users_in_groups"
#define CONFDB_NSS_FILTER_USERS "filter_users"
#define CONFDB_NSS_FILTER_GROUPS "filter_groups"
#define CONFDB_NSS_PWFIELD  "pwfield"
#define CONFDB_NSS_OVERRIDE_HOMEDIR "override_homedir"
#define CONFDB_NSS_FALLBACK_HOMEDIR "fallback_homedir"
#define CONFDB_NSS_OVERRIDE_SHELL  "override_shell"
#define CONFDB_NSS_VETOED_SHELL  "vetoed_shells"
#define CONFDB_NSS_ALLOWED_SHELL "allowed_shells"
#define CONFDB_NSS_SHELL_FALLBACK "shell_fallback"
#define CONFDB_NSS_DEFAULT_SHELL "default_shell"
#define CONFDB_MEMCACHE_TIMEOUT "memcache_timeout"
#define CONFDB_NSS_HOMEDIR_SUBSTRING "homedir_substring"
#define CONFDB_DEFAULT_HOMEDIR_SUBSTRING "/home"

/* PAM */
#define CONFDB_PAM_CONF_ENTRY "config/pam"
#define CONFDB_PAM_CRED_TIMEOUT "offline_credentials_expiration"
#define CONFDB_PAM_FAILED_LOGIN_ATTEMPTS "offline_failed_login_attempts"
#define CONFDB_DEFAULT_PAM_FAILED_LOGIN_ATTEMPTS 0
#define CONFDB_PAM_FAILED_LOGIN_DELAY "offline_failed_login_delay"
#define CONFDB_DEFAULT_PAM_FAILED_LOGIN_DELAY 5
#define CONFDB_PAM_VERBOSITY "pam_verbosity"
#define CONFDB_PAM_ID_TIMEOUT "pam_id_timeout"
#define CONFDB_PAM_PWD_EXPIRATION_WARNING "pam_pwd_expiration_warning"

/* SUDO */
#define CONFDB_SUDO_CONF_ENTRY "config/sudo"
#define CONFDB_SUDO_CACHE_TIMEOUT "sudo_cache_timeout"
#define CONFDB_DEFAULT_SUDO_CACHE_TIMEOUT 180
#define CONFDB_SUDO_TIMED "sudo_timed"
#define CONFDB_DEFAULT_SUDO_TIMED false

/* autofs */
#define CONFDB_AUTOFS_CONF_ENTRY "config/autofs"
#define CONFDB_AUTOFS_MAP_NEG_TIMEOUT "autofs_negative_timeout"

/* SSH */
#define CONFDB_SSH_CONF_ENTRY "config/ssh"
#define CONFDB_SSH_HASH_KNOWN_HOSTS "ssh_hash_known_hosts"
#define CONFDB_DEFAULT_SSH_HASH_KNOWN_HOSTS true
#define CONFDB_SSH_KNOWN_HOSTS_TIMEOUT "ssh_known_hosts_timeout"
#define CONFDB_DEFAULT_SSH_KNOWN_HOSTS_TIMEOUT 180

/* PAC */
#define CONFDB_PAC_CONF_ENTRY "config/pac"

/* Data Provider */
#define CONFDB_DP_CONF_ENTRY "config/dp"

/* InfoPipe */
#define CONFDB_IFP_CONF_ENTRY "config/ifp"
#define CONFDB_IFP_USER_ATTR_LIST "user_attributes"

/* Domains */
#define CONFDB_DOMAIN_PATH_TMPL "config/domain/%s"
#define CONFDB_DOMAIN_BASEDN "cn=domain,cn=config"
#define CONFDB_DOMAIN_ID_PROVIDER "id_provider"
#define CONFDB_DOMAIN_AUTH_PROVIDER "auth_provider"
#define CONFDB_DOMAIN_ACCESS_PROVIDER "access_provider"
#define CONFDB_DOMAIN_CHPASS_PROVIDER "chpass_provider"
#define CONFDB_DOMAIN_SUDO_PROVIDER "sudo_provider"
#define CONFDB_DOMAIN_AUTOFS_PROVIDER "autofs_provider"
#define CONFDB_DOMAIN_SELINUX_PROVIDER "selinux_provider"
#define CONFDB_DOMAIN_HOSTID_PROVIDER "hostid_provider"
#define CONFDB_DOMAIN_SUBDOMAINS_PROVIDER "subdomains_provider"
#define CONFDB_DOMAIN_COMMAND "command"
#define CONFDB_DOMAIN_TIMEOUT "timeout"
#define CONFDB_DOMAIN_ATTR "cn"
#define CONFDB_DOMAIN_ENUMERATE "enumerate"
#define CONFDB_SUBDOMAIN_ENUMERATE "subdomain_enumerate"
#define CONFDB_DEFAULT_SUBDOMAIN_ENUMERATE "none"
#define CONFDB_DOMAIN_MINID "min_id"
#define CONFDB_DOMAIN_MAXID "max_id"
#define CONFDB_DOMAIN_CACHE_CREDS "cache_credentials"
#define CONFDB_DOMAIN_LEGACY_PASS "store_legacy_passwords"
#define CONFDB_DOMAIN_MPG "magic_private_groups"
#define CONFDB_DOMAIN_FQ "use_fully_qualified_names"
#define CONFDB_DOMAIN_ENTRY_CACHE_TIMEOUT "entry_cache_timeout"
#define CONFDB_DOMAIN_ACCOUNT_CACHE_EXPIRATION "account_cache_expiration"
#define CONFDB_DOMAIN_OVERRIDE_GID "override_gid"
#define CONFDB_DOMAIN_CASE_SENSITIVE "case_sensitive"
#define CONFDB_DOMAIN_SUBDOMAIN_HOMEDIR "subdomain_homedir"
#define CONFDB_DOMAIN_DEFAULT_SUBDOMAIN_HOMEDIR "/home/%d/%u"
#define CONFDB_DOMAIN_IGNORE_GROUP_MEMBERS "ignore_group_members"
#define CONFDB_DOMAIN_SUBDOMAIN_REFRESH "subdomain_refresh_interval"

#define CONFDB_DOMAIN_USER_CACHE_TIMEOUT "entry_cache_user_timeout"
#define CONFDB_DOMAIN_GROUP_CACHE_TIMEOUT "entry_cache_group_timeout"
#define CONFDB_DOMAIN_NETGROUP_CACHE_TIMEOUT "entry_cache_netgroup_timeout"
#define CONFDB_DOMAIN_SERVICE_CACHE_TIMEOUT "entry_cache_service_timeout"
#define CONFDB_DOMAIN_AUTOFS_CACHE_TIMEOUT "entry_cache_autofs_timeout"
#define CONFDB_DOMAIN_SUDO_CACHE_TIMEOUT "entry_cache_sudo_timeout"
#define CONFDB_DOMAIN_PWD_EXPIRATION_WARNING "pwd_expiration_warning"
#define CONFDB_DOMAIN_REFRESH_EXPIRED_INTERVAL "refresh_expired_interval"

/* Local Provider */
#define CONFDB_LOCAL_DEFAULT_SHELL   "default_shell"
#define CONFDB_LOCAL_DEFAULT_BASEDIR "base_directory"
#define CONFDB_LOCAL_CREATE_HOMEDIR  "create_homedir"
#define CONFDB_LOCAL_REMOVE_HOMEDIR  "remove_homedir"
#define CONFDB_LOCAL_UMASK           "homedir_umask"
#define CONFDB_LOCAL_SKEL_DIR        "skel_dir"
#define CONFDB_LOCAL_MAIL_DIR        "mail_dir"
#define CONFDB_LOCAL_USERDEL_CMD     "userdel_cmd"

/* Proxy Provider */
#define CONFDB_PROXY_LIBNAME "proxy_lib_name"
#define CONFDB_PROXY_PAM_TARGET "proxy_pam_target"
#define CONFDB_PROXY_FAST_ALIAS "proxy_fast_alias"

struct confdb_ctx;
struct config_file_ctx;

/**
 * Data structure storing all of the basic features
 * of a domain.
 */
struct sss_domain_info {
    char *name;
    char *conn_name;
    char *provider;
    int timeout;
    bool enumerate;
    char **sd_enumerate;
    bool fqnames;
    bool mpg;
    bool ignore_group_members;
    uint32_t id_min;
    uint32_t id_max;

    bool cache_credentials;
    bool legacy_passwords;
    bool case_sensitive;

    gid_t override_gid;
    const char *override_homedir;
    const char *fallback_homedir;
    const char *subdomain_homedir;
    const char *homedir_substr;
    const char *override_shell;
    const char *default_shell;

    uint32_t user_timeout;
    uint32_t group_timeout;
    uint32_t netgroup_timeout;
    uint32_t service_timeout;
    uint32_t autofsmap_timeout;
    uint32_t sudo_timeout;

    uint32_t refresh_expired_interval;
    uint32_t subdomain_refresh_interval;

    int pwd_expiration_warning;

    struct sysdb_ctx *sysdb;
    struct sss_names_ctx *names;

    struct sss_domain_info *parent;
    struct sss_domain_info *subdomains;
    char *realm;
    char *flat_name;
    char *domain_id;
    char *forest;
    struct timeval subdomains_last_checked;

    struct sss_domain_info *prev;
    struct sss_domain_info *next;

    bool disabled;
};

/**
 * Initialize the connection to the ConfDB
 *
 * @param[in]  mem_ctx The parent memory context for the confdb_ctx
 * @param[out] cdb_ctx The newly-created connection object
 * @param[in]  confdb_location The absolute path to the ConfDB file on the
 *             filesystem
 *
 * @return 0 - Connection succeeded and cdb_ctx was populated
 * @return ENOMEM - There was not enough memory to create the cdb_ctx
 * @return EIO - There was an I/O error communicating with the ConfDB file
 */
int confdb_init(TALLOC_CTX *mem_ctx,
                struct confdb_ctx **cdb_ctx,
                const char *confdb_location);

/**
 * Get a domain object for the named domain
 *
 * @param[in] cdb The connection object to the confdb
 * @param[in] name The name of the domain to retrieve
 * @param[out] domain A pointer to a domain object for the domain given by
 *                    name
 *
 * @return 0 - Lookup succeeded and domain was populated
 * @return ENOMEM - There was insufficient memory to complete the operation
 * @return ENOENT - The named domain does not exist or is not set active
 */
int confdb_get_domain(struct confdb_ctx *cdb,
                      const char *name,
                      struct sss_domain_info **domain);

/**
 * Get a null-terminated linked-list of active domain objects
 * @param[in] cdb The connection object to the confdb
 * @param[out] domains A pointer to the first entry of a linked-list of domain
 *                     objects
 *
 * @return 0 - Lookup succeeded and all active domains are in the list
 * @return ENOMEM - There was insufficient memory to complete the operation
 * @return ENOENT - No active domains are configured
 */
int confdb_get_domains(struct confdb_ctx *cdb,
                       struct sss_domain_info **domains);


/**
 * @brief Add an arbitrary parameter to the confdb.
 *
 * This is mostly useful
 * for testing, as they will not persist between SSSD restarts. For
 * persistence, make changes to the sssd.conf file.
 *
 * @param[in] cdb The connection object to the confdb
 * @param[in] replace If replace is set to true, pre-existing values will be
 *                    overwritten.
 *                    If it is false, the provided values will be added to the
 *                    attribute.
 * @param[in] section The ConfDB section to update. This is constructed from
 *                    the format of the sssd.conf file. All sections start
 *                    with 'config/'. Subsections are separated by slashes.
 *                    e.g. [domain/LDAP] in sssd.conf would translate to
 *                    config/domain/LDAP
 * @param[in] attribute The name of the attribute to update
 * @param[in] values A null-terminated array of values to add to the attribute
 *
 * @return 0 - Successfully added the provided value(s)
 * @return ENOMEM - There was insufficient memory to complete the operation
 * @return EINVAL - The section could not be parsed
 * @return EIO - An I/O error occurred communicating with the ConfDB
 */
int confdb_add_param(struct confdb_ctx *cdb,
                     bool replace,
                     const char *section,
                     const char *attribute,
                     const char **values);

/**
 * @brief Retrieve all values for an attribute
 *
 * @param[in] cdb The connection object to the confdb
 * @param[in] mem_ctx The parent memory context for the value list
 * @param[in] section The ConfDB section to update. This is constructed from
 *                    the format of the sssd.conf file. All sections start
 *                    with 'config/'. Subsections are separated by slashes.
 *                    e.g. [domain/LDAP] in sssd.conf would translate to
 *                    config/domain/LDAP
 * @param[in] attribute The name of the attribute to update
 * @param[out] values A null-terminated array of cstrings containing all
 *                    values for this attribute
 *
 * @return 0 - Successfully retrieved the value(s)
 * @return ENOMEM - There was insufficient memory to complete the operation
 * @return EINVAL - The section could not be parsed
 * @return EIO - An I/O error occurred while communicating with the ConfDB
 */
int confdb_get_param(struct confdb_ctx *cdb,
                     TALLOC_CTX *mem_ctx,
                     const char *section,
                     const char *attribute,
                     char ***values);

/**
 * @brief Convenience function to retrieve a single-valued attribute as a
 * string
 *
 * @param[in] cdb The connection object to the confdb
 * @param[in] ctx The parent memory context for the returned string
 * @param[in] section The ConfDB section to update. This is constructed from
 *                    the format of the sssd.conf file. All sections start
 *                    with 'config/'. Subsections are separated by slashes.
 *                    e.g. [domain/LDAP] in sssd.conf would translate to
 *                    config/domain/LDAP
 * @param[in] attribute The name of the attribute to update
 * @param[in] defstr If not NULL, the string to use if the attribute does not
 *                   exist in the ConfDB
 * @param[out] result A pointer to the retrieved (or default) string
 *
 * @return 0 - Successfully retrieved the entry (or used the default)
 * @return ENOMEM - There was insufficient memory to complete the operation
 * @return EINVAL - The section could not be parsed, or the attribute was not
 *                  single-valued.
 * @return EIO - An I/O error occurred while communicating with the ConfDB
 */
int confdb_get_string(struct confdb_ctx *cdb, TALLOC_CTX *ctx,
                      const char *section, const char *attribute,
                      const char *defstr, char **result);

/**
 * @brief Convenience function to retrieve a single-valued attribute as an
 * integer
 *
 * @param[in] cdb The connection object to the confdb
 * @param[in] section The ConfDB section to update. This is constructed from
 *                    the format of the sssd.conf file. All sections start
 *                    with 'config/'. Subsections are separated by slashes.
 *                    e.g. [domain/LDAP] in sssd.conf would translate to
 *                    config/domain/LDAP
 * @param[in] attribute The name of the attribute to update
 * @param[in] defval If not NULL, the integer to use if the attribute does not
 *                   exist in the ConfDB
 * @param[out] result A pointer to the retrieved (or default) integer
 *
 * @return 0 - Successfully retrieved the entry (or used the default)
 * @return ENOMEM - There was insufficient memory to complete the operation
 * @return EINVAL - The section could not be parsed, or the attribute was not
 *                  single-valued.
 * @return EIO - An I/O error occurred while communicating with the ConfDB
 * @return ERANGE - The value stored in the ConfDB was outside the range
 *                  [INT_MIN..INT_MAX]
 */
int confdb_get_int(struct confdb_ctx *cdb,
                   const char *section, const char *attribute,
                   int defval, int *result);

/**
 * @brief Convenience function to retrieve a single-valued attribute as a
 * boolean
 *
 * This function will read (in a case-insensitive manner) a "true" or "false"
 * value from the ConfDB and convert it to an integral bool value.
 *
 * @param[in] cdb The connection object to the confdb
 * @param[in] section The ConfDB section to update. This is constructed from
 *                    the format of the sssd.conf file. All sections start
 *                    with 'config/'. Subsections are separated by slashes.
 *                    e.g. [domain/LDAP] in sssd.conf would translate to
 *                    config/domain/LDAP
 * @param[in] attribute The name of the attribute to update
 * @param[in] defval If not NULL, the boolean state to use if the attribute
 *                   does not exist in the ConfDB
 * @param[out] result A pointer to the retrieved (or default) bool
 *
 * @return 0 - Successfully retrieved the entry (or used the default)
 * @return ENOMEM - There was insufficient memory to complete the operation
 * @return EINVAL - The section could not be parsed, the attribute was not
 *                  single-valued, or the value was not a boolean.
 * @return EIO - An I/O error occurred while communicating with the ConfDB
 */
int confdb_get_bool(struct confdb_ctx *cdb,
                    const char *section, const char *attribute,
                    bool defval, bool *result);

int confdb_set_bool(struct confdb_ctx *cdb,
                     const char *section,
                     const char *attribute,
                     bool val);

/**
 * @brief Convenience function to retrieve a single-valued attribute as a
 * null-terminated array of strings
 *
 * This function will automatically split a comma-separated string in an
 * attribute into a null-terminated array of strings. This is useful for
 * storing and retrieving ordered lists, as ConfDB multivalued attributes do
 * not guarantee retrieval order.
 *
 * @param[in] cdb The connection object to the confdb
 * @param[in] ctx The parent memory context for the returned string
 * @param[in] section The ConfDB section to update. This is constructed from
 *                    the format of the sssd.conf file. All sections start
 *                    with 'config/'. Subsections are separated by slashes.
 *                    e.g. [domain/LDAP] in sssd.conf would translate to
 *                    config/domain/LDAP
 * @param[in] attribute The name of the attribute to update
 * @param[out] result A pointer to the retrieved array of strings
 *
 * @return 0 - Successfully retrieved the entry (or used the default)
 * @return ENOMEM - There was insufficient memory to complete the operation
 * @return EINVAL - The section could not be parsed, or the attribute was not
 *                  single-valued.
 * @return ENOENT - The attribute was not found.
 * @return EIO - An I/O error occurred while communicating with the ConfDB
 */
int confdb_get_string_as_list(struct confdb_ctx *cdb, TALLOC_CTX *ctx,
                              const char *section, const char *attribute,
                              char ***result);
/**
 * @}
 */
#endif