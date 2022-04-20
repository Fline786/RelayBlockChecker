@astral.command()
async def check(ctx):

    attachment_url = ctx.message.attachments[0].url

    file_request = requests.get(attachment_url)


    for url in file_request.content():
        requestURL = "https://archive.lightspeedsystems.com/SubmitDomain.php?Domain=" + url

        opener = urllib.request.FancyURLopener({})

        f = opener.open(requestURL)

        content = f.read()

        blocked = False
    
        with open("tempFile.txt", "w") as f:
            f.write(BeautifulSoup(str(content), 'html.parser').prettify())
            f.close()

        with open("tempFile.txt","r") as f:
            for l in f:
                for i in categories:
                    if i in l:
                        await ctx.send(f"{url} is blocked.")
                        blocked = True
                        break


                        
            f.close()                   
            if blocked != True:
                await ctx.send(f"{url} is not blocked.")

            os.remove("tempFile.txt")