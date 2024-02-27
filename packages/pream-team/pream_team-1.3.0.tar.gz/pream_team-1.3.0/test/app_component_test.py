from pream_team import Config


config = Config(
    token: "token",
    org_name: "org-naem",
    usernames: ["username1", "username2"],
    days_back: 10,
    cache_file_path: "cache-path",
    update_on_startup: true,
    me: "me",
    my_team: "my_team",
)

def test_startup():
    """
    mock cache file access
    mock network calls 


    when app is created

    expect ui receives cached prs for users (not older than limit)
    expect ui receives cached review requets (not older than limit)
    expect cache is cleaned up 


    when app is ran

    expect pr fetcher requets
    expect pr fetcher handles secondary rate limit 
    expect ui receives new prs for each user as they come
    expect cache saves new prs for each user as they come
    expect pr fetcher requets for 'me' & 'my-team'
    expect ui receives new prs for 'me' & 'my-team' as they come (no duplicates)
    expect cache saves new prs for 'me' & 'my-team' as they come (no duplicates)


    when handle_input with 'r' triggers update
    expect same from above

    when handle_input with 'q' triggers update
    expect ui receives stop 
    """

