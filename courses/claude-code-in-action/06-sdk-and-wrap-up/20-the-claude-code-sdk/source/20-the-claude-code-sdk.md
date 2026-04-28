# The Claude Code SDK

As we were looking at the query review hook a moment ago, we got a brief look at the CloudCode SDK.

The SDK allows you to use CloudCode programmatically.

You can use the SDK via the CLI, TypeScript library, or Python library.

This is the exact same CloudCode that you already use at the terminal.

It has all the same tools and will use them to complete a given task.

The SDK is most useful as part of a larger pipeline or tool as we saw in that hook a moment ago.

You can easily wire in CloudCode as part of a larger process to add in a bunch of intelligence to some given workflow.

Now I'd like to give you a quick demonstration of the TypeScript SDK in particular by adding it into our existing project.

Back inside of my editor, I'm going to find the sdk.ts file inside of the root project directory.

Inside of here, I put together just a little bit of code to get us started with the SDK.

I'm going to update the prompt at the top and ask Cloud to look for duplicate queries inside the src queries directory.

Then I'm going to save this file and to run it, I'll open up my terminal and execute npm run sdk.

Now this is not a built in command or anything like that.

Just so you know, behind the scenes, it just executes this file as a normal TypeScript file.

I just put together this little shortcut for us to make running a TypeScript file a little bit easier.

When we run this, we'll see the raw conversation between our local copy of Cloud code and the Cloud language model message by message.

Eventually we'll get kicked back to the command line.

The very last message printed out will contain the final response from Cloud.

Cloud.

Now there is a little bit of a gotcha around the SDK and that is that by default, it only has read abilities.

So in other words, it can only read files, directories, do grep operations and so on.

It does not have the ability to write or edit or create and so on files.

To give it right permissions.

You can either manually add in write permissions to the query call right here, or alternatively, you can add in some permission settings to your settings file inside of your dot cloud

directory.

Let me show you how we can allow the SDK to use the edit tool within this project.

I'm going to find the prompt argument right here.

Right after it, I'll add in options, put in an object, allow tools.

That'll be an array and I'll put in edit.

I'm going to update the prompt at the top and I'll ask it to add a description to the package dot JSON file.

Now I'm going to save this and run NPM run SDK once again.

And then once it is complete, I can open up the package dot JSON file and I will see that it did in fact add in a description.

So now it definitely has the ability to edit files.

As I mentioned earlier, the cloud code SDK is most useful as part of other tools.

So I would encourage you to think of opportunities to use it in helper commands scripts, or probably most notably hooks inside of your own projects.

So I'll add in a description to the next one.
