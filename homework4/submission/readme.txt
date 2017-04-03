 i. What was your strategy to defeat the target bot(s)?
    Our strategy involved abusing the network protocol between the client and server, beginning with the assumption
    that, in a client server architecture, whatever nuanced vulnerabilities existed at the application level would be
    made obvious at the network level.  That assumption was correct.

    We had a number of strategies. For example, we found a bug where whenever a client moved into a corner, the bot was
    teleported to the top left corner, so we wrote a function that continuously moved in and out of a corner and filled
    the top left corner with mines.

    Our current and most effective strategy is filling the map with normal mines, then filling the walls with + mines
    that are able to do damage inside walls. We then quickly move around the map so we're difficult to track, and we
    constantly lay a grid of mines around the enemy's coordinates.

 ii. How did you get to your solution? What triggers did you use?
    As our approach was to implement a secondary mock client, we did not rely on triggers.  Our solution was discovered
    through traffic analysis in wireshark, where we immediately noticed that every command the client sends accepts a
    name as the first param - a strong indication that server authentication "state" was open to abuse.  For example,
    the server will accept commands for any currently authenticated client regardless of origin.

 iii. A rough timeline that captures your successes and failures 
    The weekend after the homework was assigned, Brandon was able to reverse engineer most of the protocol. After
    spring break, we were able to meet up and start working on a strategy for using the API Brandon created. Over the
    next couple of days, we put together a set of functions that allowed us to defeat each bot without any
    intervention. After getting the top spot by a wide margin, we kept working on a few different attack vectors, then
    once we noticed the second place team beginning to catch up, we added functionality that would spawn a client,
    defeat a bot, and close without any human intervention. Due to the way in which the given client was designed, we
    were forced to disconnect and then reconnect after each win, which apparently caused some difficulty with the
    server and we were disallowed from playing the game any more. A screenshot is included of our score at that time.
    Moving forward, we plan on completing the mock client so we don't need to rely on the given client any longer.

 iv. What were the most significant code changes you made? Point us to the addresses in your code
    We made no changes to the given client as we reverse engineered the protocol. See mock_client.py for our work, and
    see reverse.txt for some of our early reverse engineering notes.
