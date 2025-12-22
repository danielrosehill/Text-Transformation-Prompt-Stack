The purpose of this voice note is to provide context in an audio format, as it is an audio workflow. I'll be using this audio as an internal test within the repository to test the various prompts I write for this job. This is a prompt workflow that I would describe as deceptively more challenging than it looks.

## Repository Purpose

There are a couple of purposes for this repository. It supports several different voice projects I'm working on. A common requirement I've observed over the last year of using this approach in practice is accurately prompting for text rewriting with an audio multimodal model like Gemini.

The applications and approaches I'm working on primarily use these models for voice transcription. This involves leveraging the audio understanding capability of audio multimodal models, essentially using them as a drop-in replacement for Whisper, or for Whisper followed by a large language model (LLM).

## The Voice Pipeline

The voice pipeline I've been iterating on involves sending your audio to Whisper to get a verbatim transcript. Then, you might decide you want to polish this a bit. I see two different types of polish.

The first is what I would generally regard as desirable polish. If I transcribe something with Whisper, there are a couple of edge cases where you want a verbatim reproduction of the text, such as in court proceedings. I'm sure there are many other scenarios where you need an exact copy of what was said for legal reasons. In those cases, it's probably human-based, although AI is certainly leveraged.

## Enhancing Dictation Workflows

The workflow I'm focusing on is for when I'm at my computer, and I'm replacing typing with voice. This means I want to record voice recordings intended to be sent as emails, written as blog posts, used as ReadMe files, or, increasingly, as prompts. Development prompts have probably been my major use case. It would take a long time to write out all the instructions, so it's much easier for me to start recording, go through the UI, and say "this needs fixing, this needs fixing," rather than trying to replicate that process textually by going through pages and writing notes.

The use cases really span the gamut. The core idea behind defining this prompt stack in its own repository was that as I iterated on this concept and worked through it, I came to identify different things over time that should be integrated. It truly becomes a stack of instructions. The more complex it gets, the harder it is to remember all the different things you wanted, and the less practical it becomes to do that manually.

## Programmatic Prompt Definition

The idea here is to programmatically define the levels in an orderly fashion. I'm using AI for its reasoning to ensure the order is important, not just the content. What is the appropriate sequence to send these instructions to the model so that it makes sense?

For example, one of the layers in the prompt stack is personalization. If I'm using this for writing emails in the voice notepad tool I'm currently working with, I've added a setting for the username and the user's signature. The reason I added that setting was that when writing emails, the meta-objective is to get transcriptions that are ideally ready to go without any edits needed. This goes quite a bit beyond what you might get with Whisper, which provides raw output that requires various levels of processing before you can send it.

## Avoiding Personalization Pitfalls

One pitfall I've observed in the email apps and voice notepad apps I use is that without personalization, if the model doesn't have the user's name, it will have no choice but to write "Regards, Your Name." Besides being something you need to correct, this creates the danger of not noticing it, sending the email, and it becoming embarrassing and unprofessional.

The objective of the personal information setting in the utility I'm writing this for is to provide the model with context. If we're using a model like Gemini with a lot of reasoning, I'm trying to write a prompt, a meta-prompt, that truly takes advantage of that. So, for example, if it's an email, and you have the user's name, the model should insert it, saying "Regards, Daniel" instead of "Regards, Your Name." This is reflected in the prompt stack where some instructions are inferred, meaning the model is asked to use its reasoning to infer an instruction.

## Inferred Instructions

An example of an inferred instruction is if I say, "I'm going to the supermarket today." Then I correct myself: "Wait, no, I meant to say I'm going to the pharmacy." The inference requested is that the model says, "Okay, we don't need to capture all of that." It just records the corrected text: "I'm going to the pharmacy."

Another example, which I thought of today, relates to spelling. Sometimes I spell things out. These are little things I've over the course of the year come to understand as best practices or tricks I've developed. Sometimes, if I say something that I think the AI tool is probably going to transcribe incorrectly because it's not a common word, I'll spell it out. For instance, I might say, "Today I was talking about Zod, which is a TypeScript error validator linter." And then I'll say, "Let's use Zod here. Zod is spelled Z.O.D." The desired output is simply, "Let's use Zod here." We don't need to capture the spelling instruction; we just need to infer that as an instruction. These are two examples of inferred instructions that are added into the stack.

## Grammar and Workflow Dynamics

I also made a grammatical error today. I said, "we need to add this to the list of option," instead of "options" for some reason. There's a layer in the stack that says, "correct basic text typos." It's important to realize that some of these edits, with audio understanding, significantly change the dynamic of the workflow. Because when writing these prompts, I'm thinking of the Whisper-LLM workflow, where Whisper provides something, and the model then has to say, "Hang on, that was a mistranscription."

In the case of audio multimodal, that's not applicable because the model is simultaneously processing the audio tokens and the text instructions. It's the only cook in the kitchen, which actually makes a lot of sense. Not only does it streamline the workflow, but it's also why I'm re-architecting from Whisper to this approach.

## Voice Notepad and Gemini Integration

As an aside, the tool I'm using, Voice Notepad on GitHub, is actually a prototype in action. I've been using it for a couple of weeks now, and I've processed over 800 transcriptions. This means I'm using it for everything—little bursts of things, mostly prompts (I'd say 80%). I've spent about one or two dollars on the Open Router API, which I'm using simply because it allows me to track my expenditure at the key level, which Gemini doesn't. So I can issue an API key just for this app, go into the cost tracking, and see precisely how much I've spent across all models.

That's not even using the cheapest Gemini model; I'm using Gemini Flash 2.5 regular. There's also Pro and Light, and Gemini 3. To be honest, I don't see any reason at that cost level for me personally to try to do it any cheaper; that's more than acceptable. There's also no compelling reason to use Pro because it's doing a good enough job. In fact, it would probably be a total waste. I would say that the model Google would probably recommend itself for this workflow is Light, because you just need something that can process audio tokens and process your instruction.

## Cost Optimization and Prompt Caching

The only cost optimization I can think of that would actually make sense here is prompt caching. This is because the general cleanup prompt, in the way I'm envisioning this, is quite extensive but also repetitive. So, if I'm recording a short transcript like, "Let's take this UI and let's edit the CSS and add these, change these colors to this," that would be a very short prompt. It's kind of stupid to send five seconds of audio alongside a 600-word prompt defining all the "if it says this, change this." It's overkill.

This is an engineering question. Maybe it's a frontend thing that I want to have: if the audio is very short, we'll send a short cleanup prompt, and if it's more than one minute, we'll send a bigger one. But the only real reason for that would be cost optimization because it doesn't make sense to me. However, when you're talking about the costs, they are so little that it almost just makes more sense to process the text.

## Vision for a Long Note

This is the sample audio I've created as an example of a long note. What I'm recording this for, beyond explaining the idea here, is for versioning the general cleanup prompt. The reason I'm doing this in a version-controlled way is that, as I mentioned, it's mostly static, but I do make tweaks over time, like the one today. For example, when I'm getting back a transcript in the course of using this system myself, I might see something like "ZOD" and think, "Wait, I should add that as an instruction because I don't need to see that. I just want to have that applied."

## The Prompt Constructor

There's going to be a constructor here. The most important thing I want to do is define the sequence of the constructed, consolidated, or concatenated prompt that makes the most sense. I think that's important not just for presentation, but I also want to give the LLM better input. I want to add subheadings, which is another addition I'm making today. Based on what I've noticed working with LLMs, they love structure. The more you can help them with headings and subheadings, the better adherence you'll get—that's my theory, and I think there's some evidence for it.

## Generating Prompts with Variance

Finally, the second thing is generating out the constructed prompts with variance. I've tried to divide it at the top level between foundational and specific prompts. Specific ones being that there's actually a whole world of permutations you can do here in the realm of specific prompts, and I'm sure I've only thought of a few of them.

The ones I use in this application that I'm trying to present as the few ones you'll want to use 90% of the time are: to-do list, system prompt, user prompt, and development prompts. Something else that I would say, by way of another aside, maybe if we tune the prompt a bit for thought organization, we can make my own notes here a bit more organized.

## The Power of a Good System Prompt

By way of another aside, what I've noticed over time is that if you can really get the general system prompt very effective, a lot of these distinctions don't really matter. An AI prompt, in a sense, is specific, yes, but to a greater extent, it adheres to the principles of good writing. So if you can have a good foundational prompt that cleans up the filler words, adds subheadings, and resolves typos, the rest of it is probably going to be suitable as an AI prompt without you needing to say "add in like optimize this for its intended use as an AI prompt."

## Email Formatting Specificity

For email, it's a little bit more. That's one area where I definitely see a need for format-specific instruction because an email needs to be written in a format like "Dear X." You want to have short paragraphs. That's also for the stylistic instructions, where I have presets for business-appropriate and casual-appropriate. Those are more the cases where if you don't have that added tweak in the format-specific versions, it can go off. You don't want to write something really casual in a work email.

## Background Interruption and Inferred Removal

[Background audio: picking up son]

I just mentioned I'm picking up my son Ezra. I'm now carrying him, and I'm holding up my phone to dictate. I probably don't need that in the transcript. I don't even know why I said it; I'm just in the habit of it, I guess. I feel like I'm recording this in case someone might want to listen to it. But depending on the context, that could probably be safely scrubbed.

Another one in the inferred instruction category is when you're transcribing or dictating something, you might, for example, be in an office context. A friend bumps in and says, "Oh, hey Daniel." And then you'd gesture to your microphone and say, "Hey, I'm in the middle of something. Can we do this later?" Again, an example of something that with audio understanding, the model can actually hear. That was a different person. And I'm asking it to reason to say we don't need that in the transcript. If the user was recording a blog instruction or a document, we don't need to get the part where the friend popped into the office and the user responded, or the DHL guy, etc.

So, this category of inferred instructions for removal, I would say this is actually deductive logic. This is asking the AI tool, the reasoning model, to deduce that we don't need this.

## Pure Inferred Logic and Risk

Speaking of pure inferred logic, another one I thought of today, and this is again where this workflow gets risky, is that the more you're asking an AI model to use its own reasoning, potentially the more useful it is. But the potential for it to destroy the transcript gets higher. It's a gamble, basically.

But the one I thought of today was as maybe an alternative to the stylistic instruction prompt concatenation whereby the user selects a button saying "this is an email." The AI model is asked to deduce that itself. The user might say, "This is an email to my boss." The AI tool can say, "Okay, this is context. That's a formatting directive, and I'm going to provide the transcript with that in mind." It will therefore make sure it's business-appropriate and include the user's email signature. That's much more elegant, in fact, and I think probably that's the end goal for this pattern in implementation because that would eliminate the need for buttons entirely if the user could just speak and define the need, and we don't need to have a button for the user to have to use to define the purpose.

## Advanced Use Cases and Machine Readability

The other one would be, at a more ambitious level of scale, sometimes I've thought about capturing stuff in JSON. Like I might define something I see or I'm recording some information. I'm trying to think... it's kind of a very marginal idea, but you could say, "I'm creating a home inventory system, and I want to record what's in my house." And looking around, "Here's what I see." Then the constructed prompt might be, "Create a JSON array for the categories of goods in the user's house." And that might be used to jumpstart the development of a home inventory system.

But again, these are edge cases, but ones that are particularly interesting because they open up the possibility that the transcripts can not only be human-readable but also machine-readable for use in AI applications. But the main workflow I'm working on is actually doing that as a second layer, as a processing layer, in order that we can connect these voice transcripts to AI tools. This is more a pure utility for humans to use.

## The Prompt Stack Concept

I think that pretty much covers the concept behind the prompt stack, as I call it, and the reason that there's a divergence between what I call the foundational one. The other kind of meta-type, if you will, is actually a verbatim transcript. With a model like Whisper, an ASR model, you don't need to do anything to get that; that's what you're going to get by default. You're going to get a verbatim transcript.

With an audio multimodal model with audio understanding, unless the API is designed to accommodate this, you need to tell the model what to do with that audio. If I just send audio without any prompt, it doesn't know, "Well, what do you want? Do you want me to identify the speaker?" So to get a verbatim transcript with audio multimodal, you actually need to explicitly create a verbatim transcript prompt. Therefore, that's one that I wanted to include in the app I'm working on.

## Verbatim Transcripts with Audio Multimodal

There are again use cases for that. I would say in general, it makes much less sense with audio multimodal for the simple reason that if that was your objective, you'd probably just be using a traditional ASR approach. But if you were happy to gamble on audio multimodal for all of this, you might have that as a prompt. It's going to be, again, less because you're prompting for that. I think it's going to be less 100% robust than Whisper would be. But there might be some uses, and therefore that's one that I have in the app as well that I want to include in the pipeline.

## Main Workflow and Presets

The main one, I would say, the 90% what I've discovered in this is that all these presets that I've thought of, and I didn't even get into them, there's a bunch of them. You could play around with word constraints. The general flow in the prompt stack is that these would come after the foundational. Again, that's why it's called a stack.

For the stylistic ones, let's say I have one to "make the writing as formal as possible." The intended stack would be: send in "remove the filler words," "add the punctuation," "add the paragraphs," then "make the language as formal as possible." So they're additive to the foundational. Ideally, in the front end, the prompt construction or concatenation logic I've developed allows you to use multiple ones. That's where the order of construction again becomes important, because in addition to just defining them, you want to present them in a logical manner.

## Managing Conflicting Instructions

To give another example of an additive stack that has elements to it, we would have, "I want it to be formal and persuasive." Two things: formal is a writing style, persuasive is another writing style that's going to affect the selection of language. So that stack might be called, in the front-end label, "Formal and Persuasive."

The actual stack or prompt rewriting stack that would get sent to the audio multimodal model in this case would be:
1. Here's the audio data.
2. The user's name is Daniel (this is being injected through the personalization).
3. Here are the general instructions for how you should transcribe this audio into text (going through all the foundational elements we've discussed here).
4. Make the text as formal as possible.
5. Make the text as persuasive as possible.

What we want in the prompt concatenation logic is probably to avoid introducing conflicts. We don't want, firstly, to introduce the more elaborate this becomes, the greater the chance that we're going to have internal logical conflicts. For example, we can't have the main cleanup prompt say it should be "as easy to read as possible," and then have it say it should be "as formal as possible." They're kind of oppositional.

So, without getting too lost in the complication of this idea, the actual prompt construction logic might itself need to rely upon AI to say, "You've got these three ingredients, as it were." And we want to create a constructed prompt. The answer might be that these constructed meta-prompts, instead of being injected dynamically, are predefined so that if there are any potential internal disagreements, they are resolved. And whatever tool I'm using for this transcription process has a bunch of presets ready that are validated so everything's in harmony. It's doing all the jobs, and you just send something and you get back something exactly meeting our expectations—that's the objective here.

## Conclusion and Audio Preprocessing

I'll have to leave it at that, as I'm getting fatigued from carrying around this little guy. But that's the idea here, and this lengthy audio file, which is actually quite reflective, is about 25 minutes; it will probably hit 30. It will be good to demonstrate two things. Number one, that audio multimodal is very capable. I've used it for one hour. The challenge is actually, there is a theoretical audio length limit—sorry, not theoretical, it's documented—but it's like multiple hours. It's very unlikely that someone's going to hit it in this use.

The more pertinent one is an audio file size limit. I think Gemini's is 20 megabytes. So what I do in my implementation is pre-processing. VAD (Voice Activity Detection) to cut out silence, and then getting it down to audio-friendly format. That generally means going from stereo to mono, compressing it to Opus. Usually, that's enough. That's generally enough that if you record something in WAV for audio, it's going to be downsampled anyway, so there's no point. You do these pre-processing steps, and then you hit the API well under the limit, well under the audio size limit, and you get back audio processing.

That's where the final thing I'll say: I've tried local models for this. There are a few that can run, and it just wasn't possible. Because, I think, this approach is very computationally heavy. In the sense that if you're sending something in one go, chunking doesn't even really make sense. So you're asking it to hold a huge amount of context there. And I find with my own attempts, I think I got Vax for running, but it just couldn't—I couldn't contain it. The GPU just ran out of memory, and even with attempts to use chunking, that kind of had its own problems. So I just, because the costs are so little as well, it's not an approach I'm really going to look into at all. In general, my preference for voice stuff, I actually much prefer to use cloud inference. I just think, and I understand there are different reasons people don't want to do that, like privacy, but I'm not worried about that particularly. So for me, the costing doesn't really justify the complexity, and more than the complexity, using those less performant models.

That's all the details about this process. We will send it for transcription now.

Daniel Rosehill