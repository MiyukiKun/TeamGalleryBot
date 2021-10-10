def parse_arg(arg):
    arg = arg.lower()
    arg = arg.replace(" ","")
    arg = arg.replace("_","")
    return arg

def parse_about(about):
    unwanted_shit = ["Manga: @Manga_Gallery","Anime: @Anime_Gallery", "Group: @Anime_Discussion_Cafe", "Animes: @Anime_Gallery", "Anime:@Anime_Gallery", "Animes:@Anime_Gallery", "Group:@Anime_Discussion_Cafe", "Group: @MangaTards", "Group:@MangaTards"]
    about = about.split("\n")
    try:
        for i in unwanted_shit:
            if i in about:
                about.remove(i)
    except:
        pass
    return "\n".join(about)  