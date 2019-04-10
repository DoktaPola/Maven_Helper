# Maven Helper
The Maven Helper is a utility Python script written to help with the distribution of the Maven artifacts between users that work remotely.
In particular, the script can help with the process when first user (will be called 'local' one) receives some Maven-based Java project from the second, customer-side user (will be called 'remote' one) and finds out that he doesn't have some library L in his Maven directory. He could request that library L to be sent to him by remote user, but the problem here is that artifact L might in its turn have its dependencies D1, D2, ... , Dn, which might also be absent in local user's Maven directory; so these dependencies need to be sent to local user from remote user as well. As Maven doesn't report that in addition to the artifact L it would be also required to provide dependent artifacts D1, D2, ... , Dn, the process of delivering the artifact L together with all missing dependencies from remote user to local user might be iterative, requiring additional efforts.
The Maven Helper was developed to solve that problem and allow more convenient single-iteration transferring of artifact L and its missing dependencies D1, D2, ... , Dn from remote user to the local user.

### Usage

This app can be used in ***two*** modes.

The first one is for **local** requests.
User should enter:

```
--snapshot-maven-local-repo, full_path_to_snapshot_file, full_path_to_Maven_folder.

Example: --snapshot-maven-local-repo C:\PycharmProjects\MavenHelper\SNAPSHOT C:\MAVEN_HELPER\local
```

The second mode is for **remote** requests.
User should enter:
```
--pack-missing-artifact-deps, missing_library, full_path_to_snapshot_file, full_path_to_Maven_folder, full_path_where_finale_archive_with_dependencies.

--pack-missing-artifact-deps org\apache\jena\jena-tdb2\3.8.0 C:\PycharmProjects\MavenHelper\SNAPSHOT C:\MAVEN_HELPER\remote C:\MAVEN_HELPER\MY_AR.zip
```
! Please note that SNAPSHOT FILE comes to the remote user from the local user, after calling of this app in thr local mode. Then the local user should send this file to the remote user with missing artifact.

!! ZIP file will be located on this path --> full_path_where_finale_archive_with_dependencies
