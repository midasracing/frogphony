import { useCallback, useEffect, useRef, useState } from 'react';
import {
  useRive,
  useViewModelInstanceTrigger,
  Layout,
  Fit,
  Alignment,
} from '@rive-app/react-webgl2';

export type KumkaAction = 'blink' | 'look' | 'wave' | 'success';
export type KumkaCue = { type: KumkaAction; id: number };

type Props = {
  className?: string;
  cue?: KumkaCue;
  alt?: string;
};

const layout = new Layout({ fit: Fit.Contain, alignment: Alignment.Center });

export default function Kumka({ className = '', cue, alt = 'Kumka, różowa ropucha' }: Props) {
  const [loaded, setLoaded] = useState(false);
  const [loadFailed, setLoadFailed] = useState(false);
  const motionRef = useRef<HTMLDivElement>(null);
  const lastPlayedId = useRef<number | null>(null);
  const onLoad = useCallback(() => { setLoaded(true); setLoadFailed(false); }, []);
  const onLoadError = useCallback(() => {
    setLoadFailed(true);
    setLoaded(false);
    console.warn('Frogphony: Rive did not load; animated mascot fallback is active.');
  }, []);

  const { rive, RiveComponent } = useRive({
    src: `${import.meta.env.BASE_URL}animations/kumka.riv`,
    artboard: 'Kumka',
    stateMachine: 'KumkaController',
    autoplay: true,
    autoBind: true,
    layout,
    shouldDisableRiveListeners: true,
    onLoad,
    onLoadError,
  });

  const instance = rive?.viewModelInstance;
  const { trigger: blink } = useViewModelInstanceTrigger('blink', instance);
  const { trigger: look } = useViewModelInstanceTrigger('look', instance);
  const { trigger: wave } = useViewModelInstanceTrigger('wave', instance);
  const { trigger: success } = useViewModelInstanceTrigger('success', instance);

  // The native Rive trigger controls the eyes, bones and expression.
  useEffect(() => {
    if (!rive || !cue || cue.id === lastPlayedId.current) return;
    const triggers = { blink, look, wave, success };
    const fire = triggers[cue.type];
    if (fire) {
      fire();
      lastPlayedId.current = cue.id;
    }
  }, [rive, cue, blink, look, wave, success]);

  // A clearly visible whole-body motion also acts as an animated fallback
  // when WebGL/Rive cannot play on a particular device.
  useEffect(() => {
    if (!cue) return;
    const element = motionRef.current;
    if (!element) return;
    element.classList.remove('kumka-cue-wave', 'kumka-cue-blink', 'kumka-cue-look', 'kumka-cue-success');
    // Restart the animation even when the same trigger is fired twice.
    void element.offsetWidth;
    element.classList.add(`kumka-cue-${cue.type}`);
  }, [cue]);

  return (
    <div className={`kumka-rive ${className}`} role="img" aria-label={alt}>
      <div ref={motionRef} className="kumka-motion">
        {!loaded && (
          <img className="kumka-fallback" src={`${import.meta.env.BASE_URL}kumka.png`} alt="" />
        )}
        {!loadFailed && <RiveComponent className="kumka-canvas" aria-hidden="true" />}
      </div>
    </div>
  );
}
