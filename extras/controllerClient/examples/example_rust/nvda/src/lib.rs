pub use nvda_bindgen::{error_status_t, wchar_t};
use nvda_bindgen::{
    nvdaController_brailleMessage, nvdaController_cancelSpeech, nvdaController_getProcessId,
    nvdaController_setOnSsmlMarkReachedCallback, nvdaController_speakSsml,
    nvdaController_speakText, nvdaController_testIfRunning, onSsmlMarkReachedFuncType,
    SPEECH_PRIORITY, SYMBOL_LEVEL,
};
use windows::{
    core::{Result, HSTRING},
    Win32::Foundation::{ERROR_SUCCESS, WIN32_ERROR},
};

#[repr(u32)]
#[derive(Debug, Copy, Clone, Hash, PartialEq, Eq)]
pub enum SpeechPriority {
    Normal = 0,
    Next = 1,
    Now = 2,
}

#[repr(i32)]
#[derive(Debug, Copy, Clone, Hash, PartialEq, Eq)]
pub enum SymbolLevel {
    None = 0,
    Some = 100,
    Most = 200,
    All = 300,
    Char = 1000,
    Unchanged = -1,
}

pub type OnSsmlMarkReached = onSsmlMarkReachedFuncType;

pub fn test_if_running() -> Result<()> {
    let res = WIN32_ERROR(unsafe { nvdaController_testIfRunning() });
    if res != ERROR_SUCCESS {
        return Err(res.into());
    }
    Ok(())
}

pub fn cancel_speech() -> Result<()> {
    let res = WIN32_ERROR(unsafe { nvdaController_cancelSpeech() });
    if res != ERROR_SUCCESS {
        return Err(res.into());
    }
    Ok(())
}

pub fn speak_text(text: &str, interrupt: bool) -> Result<()> {
    if interrupt {
        cancel_speech()?
    }
    let text = HSTRING::from(text);
    let res = WIN32_ERROR(unsafe { nvdaController_speakText(text.as_ptr()) });
    if res != ERROR_SUCCESS {
        return Err(res.into());
    }
    Ok(())
}

pub fn braille_message(mesage: &str) -> Result<()> {
    let message = HSTRING::from(mesage);
    let res = WIN32_ERROR(unsafe { nvdaController_brailleMessage(message.as_ptr()) });
    if res != ERROR_SUCCESS {
        return Err(res.into());
    }
    Ok(())
}

pub fn get_process_id() -> Result<u32> {
    let mut pid: u32 = 0;
    let res = WIN32_ERROR(unsafe { nvdaController_getProcessId(&mut pid) });
    if res != ERROR_SUCCESS {
        return Err(res.into());
    }
    Ok(pid)
}

fn set_on_ssml_mark_reached_callback(callback: OnSsmlMarkReached) -> Result<()> {
    let res = WIN32_ERROR(unsafe { nvdaController_setOnSsmlMarkReachedCallback(callback) });
    if res != ERROR_SUCCESS {
        return Err(res.into());
    }
    Ok(())
}

pub fn speak_ssml(
    ssml: &str,
    symbol_level: SymbolLevel,
    priority: SpeechPriority,
    asynchronous: bool,
    callback: onSsmlMarkReachedFuncType,
) -> Result<()> {
    if callback.is_some() {
        set_on_ssml_mark_reached_callback(callback)?
    }
    let ssml = HSTRING::from(ssml);
    let res = WIN32_ERROR(unsafe {
        nvdaController_speakSsml(
            ssml.as_ptr(),
            symbol_level as SYMBOL_LEVEL,
            priority as SPEECH_PRIORITY,
            asynchronous.into(),
        )
    });
    if res != ERROR_SUCCESS {
        return Err(res.into());
    }
    if callback.is_some() {
        set_on_ssml_mark_reached_callback(None)?
    }
    Ok(())
}
