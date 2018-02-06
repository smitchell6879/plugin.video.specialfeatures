# plugin.specialfeatures
Inspired by the new bluray features of Kodi 18; This addon will present all of the bonus videos, discs, versions you have of movies in your library.


You will need to create a 'Extras' Folder in the 'Root' folder of each movie that you will be adding special features too.

eg.
```
    The Pirates of the Caribbean\
                                  >BDMV
                                  >CERTIFICATE
                                  >Extras
                                  >poster.jpg
                                  fanart.jpg
```

Once you have made the Extras folder you may place individual video clips, Full Bluray and DVD rips

```
The Pirates of the Caribbean\Extras\
                                    >Theactrical Trailer .mkv/mp4/ etc
                                    >3D Verison\BDMV\index.bdmv
                                    >Bonus Disc\VIDEO_TS\VIDEO_TS.IFO
```
Using the Context Menu.. 
        The Menu is only availble if the selected item has extras availiable and has been scaned into the addons database.
        This could solve the issuse with people having multiple verisons of the same movie, just open the context menu and select
        'Special Features'... If this becomes a popular use for this addon i can modify it to have a seperate folder check so not to
        mix different verisons with special features.
        
There is a Service that has to be ran for the context menu and Video Info to work so i recommend after installing to close and restart kodi.

RECOMMEND ADVANCED USER SETTING

```  
<advancedsettings>
    <video>
        <!-- VideoExtras: Section Start -->
        <excludefromscan action="append">
            <regexp>/Extras/</regexp>
            <regexp>[\\/]Extras[\\/]</regexp>
        </excludefromscan>
        <excludetvshowsfromscan action="append">
            <regexp>/Extras/</regexp>
            <regexp>[\\/]Extras[\\/]</regexp>
        </excludetvshowsfromscan>
        <!-- VideoExtras: Section End -->
    </video>
</advancedsettings>
```
###########################################################################################

This plugin can be called when a listitem is selected using RunScript(plugin.specialfeatures,listitem)

You can use this in a widget simply with:

```
plugin://plugin.specialfeatures/
```
This will return a list of movies with extras, the same thing you get when selecting the addon.

############################################################################################
Support added for MYSQL SERVER has been tested on MySQL 5.7

Assuming you already have MySQL setup and running simply go to addon settings
MySQL tab and enter your information and run the addon simple as that.
