# plugin.specialfeatures
Inspired by the new bluray features of Kodi 18; This addon will present all of the bonus videos, discs, versions you have of movies in your library.


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

