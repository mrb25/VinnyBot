package com.bot;

import com.sedmelluq.discord.lavaplayer.player.AudioPlayerManager;
import com.sedmelluq.discord.lavaplayer.player.DefaultAudioPlayerManager;
import com.sedmelluq.discord.lavaplayer.source.AudioSourceManagers;
import net.dv8tion.jda.core.AccountType;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.JDABuilder;
import net.dv8tion.jda.core.entities.Member;
import net.dv8tion.jda.core.hooks.ListenerAdapter;
import com.sedmelluq.discord.lavaplayer.player.AudioLoadResultHandler;
import com.sedmelluq.discord.lavaplayer.tools.FriendlyException;
import com.sedmelluq.discord.lavaplayer.track.AudioPlaylist;
import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import net.dv8tion.jda.core.entities.Guild;
import net.dv8tion.jda.core.entities.TextChannel;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import net.dv8tion.jda.core.managers.AudioManager;

/**
 * Created by Jess Walter on 3/28/2017.
 */

import java.util.HashMap;
import java.util.Map;

public class Bot extends ListenerAdapter {
    private static String nickName;
    private static String avatarURL;

    public static void main(String[] args) throws Exception {
        Config config = new Config();
        JDA jda = new JDABuilder(AccountType.BOT)
                .setToken(config.getToken("Discord"))
                .buildBlocking();

        jda.addEventListener(new Bot());
        nickName = jda.getSelfUser().getName();
        avatarURL = jda.getSelfUser().getAvatarUrl();
    }

    private final AudioPlayerManager playerManager;
    private final Map<Long, ServerMusicManager> musicManagers;


    private Bot() {
        this.musicManagers = new HashMap<>();

        this.playerManager = new DefaultAudioPlayerManager();
        AudioSourceManagers.registerRemoteSources(playerManager);
        AudioSourceManagers.registerLocalSource(playerManager);
    }

    private synchronized ServerMusicManager getServerAudioPlayer(Guild guild) {
        long guildId = Long.parseLong(guild.getId());
        ServerMusicManager musicManager = musicManagers.get(guildId);

        if (musicManager == null) {
            musicManager = new ServerMusicManager(playerManager);
            musicManagers.put(guildId, musicManager);
        }

        guild.getAudioManager().setSendingHandler(musicManager.getSendHandler());

        return musicManager;
    }

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        String[] command = event.getMessage().getContent().split(" ", 2);
        Guild guild = event.getGuild();

        if (guild != null) {
            if ("~play".equals(command[0]) && command.length == 2) {
                if (event.getMember().getVoiceState().getChannel() == null){
                    event.getTextChannel().sendMessage("You are not connected to a voice channel :cry:").queue();
                    return;
                }
                loadAndPlay(event.getTextChannel(), command[1], event.getMember());
            } else if ("~skip".equals(command[0])) {
                skipTrack(event.getTextChannel());
            } else if ("~playlist".equals(command[0])) {
                getPlaylist(event.getTextChannel());
            } else if ("~stop".equals(command[0])) {
                stopPlayer(event.getTextChannel());
            } else if ("~pause".equals(command[0])) {
                pauseTrack(event.getTextChannel());
            } else if ("~resume".equals(command[0])) {
                resumeTrack(event.getTextChannel());
            } else if ("~voicestats".equals(command[0])) {
                voiceStats(event.getTextChannel());
            } else if ("~search".equals(command[0])){
                //search(event.getTextChannel(), command[1], event.getMember());
                event.getTextChannel().sendMessage("Search functionality coming soon. Checkout the discord server for frequent updates.").queue();
            }
        }

        super.onMessageReceived(event);
    }

    private void loadAndPlay(final TextChannel channel, final String trackUrl, final Member author) {
        final ServerMusicManager musicManager = getServerAudioPlayer(channel.getGuild());

        playerManager.loadItemOrdered(musicManager, trackUrl, new AudioLoadResultHandler() {
            @Override
            public void trackLoaded(AudioTrack track) {
                channel.sendMessage("Adding to queue " + track.getInfo().title).queue();

                play(channel.getGuild(), musicManager, track, author);
            }

            @Override
            public void playlistLoaded(AudioPlaylist playlist) {
                AudioTrack firstTrack = playlist.getSelectedTrack();

                if (firstTrack == null) {
                    firstTrack = playlist.getTracks().get(0);
                }

                channel.sendMessage("Adding to queue " + firstTrack.getInfo().title + " (first track of playlist " + playlist.getName() + ")").queue();

                play(channel.getGuild(), musicManager, firstTrack, author);
            }

            @Override
            public void noMatches() {
                channel.sendMessage("Nothing found by " + trackUrl).queue();
            }

            @Override
            public void loadFailed(FriendlyException exception) {
                channel.sendMessage("Could not play: " + exception.getMessage()).queue();
            }
        });
    }

    private void play(Guild guild, ServerMusicManager musicManager, AudioTrack track, final Member author) {
        connectToVoiceChannel(guild.getAudioManager(), author);

        musicManager.scheduler.queue(track);
    }

    private void skipTrack(TextChannel channel) {
        ServerMusicManager musicManager = getServerAudioPlayer(channel.getGuild());
        musicManager.scheduler.nextTrack();

        channel.sendMessage("Skipped to next track.").queue();
    }

    private static void connectToVoiceChannel(AudioManager audioManager, final Member author) {
        if (!audioManager.isConnected() && !audioManager.isAttemptingToConnect()) {
                audioManager.openAudioConnection(author.getVoiceState().getChannel());
        }
    }

    private void pauseTrack(final TextChannel textChannel){
        ServerMusicManager musicManager = getServerAudioPlayer(textChannel.getGuild());
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio").queue();
            return;
        }
        musicManager.scheduler.pause();
        textChannel.sendMessage("Successfully paused stream").queue();
    }

    private void resumeTrack(final TextChannel textChannel) {
        ServerMusicManager musicManager = getServerAudioPlayer(textChannel.getGuild());
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio").queue();
            return;
        }
        musicManager.scheduler.resume();
        textChannel.sendMessage("Successfully resumed Stream").queue();
    }

    private void stopPlayer(final TextChannel textChannel) {
        ServerMusicManager musicManager = getServerAudioPlayer(textChannel.getGuild());
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio").queue();
            return;
        }
        musicManager.scheduler.stopPlayer();
        textChannel.getGuild().getAudioManager().closeAudioConnection();
        textChannel.sendMessage("Stopping player").queue();
    }

    private void getPlaylist(final TextChannel textChannel) {
        ServerMusicManager musicManager = getServerAudioPlayer(textChannel.getGuild());
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio").queue();
            return;
        }
        else {
            String[] playlist = musicManager.scheduler.getPlaylist();
            String msg = "```Playlist\n";
            for (int i = 0; i < playlist.length; i++){
                if (i == 0)
                    msg += "Now Playing: " + playlist[i] + "\n";
                else if (i == 1) {
                    msg += "Next: " + playlist[i] + "\n";
                }
                else
                    msg += (i+1) + ": " + playlist[i] + "\n";
            }
            msg += "```";
            textChannel.sendMessage(msg).queue();
        }
    }

    private int getNumberActiveStreams() {
        int count = 0;
        for (Map.Entry<Long, ServerMusicManager> entry : musicManagers.entrySet()) {
            ServerMusicManager manager = entry.getValue();
            if (manager.scheduler.isPlaying()) {
                count++;
            }
        }
        return count;
    }

    private void voiceStats(TextChannel textChannel) {
        int activeServers = getNumberActiveStreams();
        int totalServers = musicManagers.size();
        EmbedBuilder builder = new EmbedBuilder();
        builder.setAuthor(nickName, avatarURL, avatarURL);
        builder.addField("Total voice servers", "" + totalServers, true);
        builder.addField("Active voice servers", "" + activeServers, true);
        builder.addField("Memory used", "" + (((Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory())/1024)/1024) + " MB", true);
        textChannel.sendMessage(builder.build()).queue();
    }


    private void search(final TextChannel channel, final String trackUrl, final Member author) {
        final ServerMusicManager musicManager = getServerAudioPlayer(channel.getGuild());

        playerManager.loadItemOrdered(channel.getGuild(), "ytsearch:"+trackUrl, new AudioLoadResultHandler() {
            @Override
            public void trackLoaded(AudioTrack track) {
                channel.sendMessage("Adding to queue " + track.getInfo().title).queue();

                play(channel.getGuild(), musicManager, track, author);
            }

            @Override
            public void playlistLoaded(AudioPlaylist playlist) {
                int i = 1;
                EmbedBuilder builder = new EmbedBuilder();
                builder.setTitle("Search results", "");
                builder.addField("Select a song to add by reacting with the corresponding number", "", false);
                for (AudioTrack track : playlist.getTracks()){
                    builder.addField("", i + ": " + track.getInfo().title, false);
                }
                channel.sendMessage(builder.build()).queue();
            }

            @Override
            public void noMatches() {
                channel.sendMessage("Nothing found for " + trackUrl).queue();
            }

            @Override
            public void loadFailed(FriendlyException exception) {
                channel.sendMessage("Could not play: " + exception.getMessage()).queue();
            }
        });
    }
}