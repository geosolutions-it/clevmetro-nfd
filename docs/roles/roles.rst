.. _roles:

==============================
Managing Permissions and Roles
==============================

.. toctree::
   :hidden: 
   :maxdepth: 4

The authentication and the authorization services are based on **LDAP** (Lightweight Directory Access Protocol). LDAP is an industry standard application for accessing 
and maintaining distributed directory information services over an Internet Protocol network. It plays the role as a central place to store usernames and passwords which allows 
many different applications and services to connect to the LDAP server to validate users.

Authentication
==============

The Cleveland Metroparks LDAP Server tree is implemented as in the figure below: 

 .. figure:: img/LDAP_tree.png
    :scale: 75 %

In the figure above, assigning the user *uid* as an attribute in the *memberUid* field of a certain group, the user will make part automatically of that group. Moreover, 
it will be authenticated to compute some operations according to its role. Anonymous users can not access any of the NFD data.


 .. literalinclude:: LDAP_example.txt

   

Authorization
=============

Groups and Roles
****************

The existing features in the portal are **Animals**, **Plants**, **Fungi**, **Slime mold**, and **Natural areas**. Each feature has two corresponding groups on 
LDAP tree **Feature_Writer** and **Feature_Publisher** (e.g. **Animals_Writer** and **Animals_Publisher**). 

**Feature_Writer** members are allowed to **add** new features belonging to that group, which will be saved but **not published** by default. 
They are allowed to **edit** their own features and to **edit** features added by other members belonging to that group. Modifying an existing feature will create 
automatically a **new version** of that feature and will automatically **unpublish** it. 

 .. note:: Unpublished features won't be visible to other users not belonging to that group. 
 
**Feature_Publisher** members can **view** all the features belonging to that group and accordingly if unpublished they can **publish** it. This allows other authenticated 
users to access them (beyond the author and the rest of members of the **Feature_Writer** or **Feature_Publisher**). 

 .. note:: Only **published** features are visible (in READ only mode) to authenticated users not belonging to any of the above groups for the specific feature. 
 
A user can be a member of both, just one or none of the above groups for each feature. 






