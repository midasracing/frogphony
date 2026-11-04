import { useEffect, useRef } from 'react';
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
  onClick?: () => void;
};

// Rive's artboard and triggers are defined in design/kumka-animation/rig-manifest.json.
// Keep the PNG as a fallback if WebGL or the .riv file is not available.
export default function Kumka({ className = '', cue, alt = 'Kumka, różowa ropucha', onClick }: Props) {
  const { rive, RiveComponent } = useRive({
    src: `${import.meta.env.BASE_URL}animations/kumka.riv`,
    artboard: 'Kumka',
    stateMachines: 'KumkaController',
    autoplay: true,
    autoBind: true,
    layout: new Layout({ fit: Fit.Contain, alignment: Alignment.Center }),
    shouldDisableRiveListeners: true,
  });
  const instance = rive?.viewModelInstance;
  const { trigger: blink } = useViewModelInstanceTrigger('blink', instance);
  const { trigger: look } = useViewModelInstanceTrigger('look', instance);
  const { trigger: wave } = useViewModelInstanceTrigger('wave', instance);
  const { trigger: success } = useViewModelInstanceTrigger('success', instance);
  const lastPlayedId = useRef<number | null>(null);

  useEffect(() => {
    if (!rive || !cue || cue.id === lastPlayedId.current) return;
    const triggers = { blink, look, wave, success };
    const fire = triggers[cue.type];
    if (!fire) return;
    fire();
    lastPlayedId.current = cue.id;
  }, [rive, cue, blink, look, wave, success]);

  return (
    <div className={`kumka-rive ${className}`} role="img" aria-label={alt}
      onClick={onClick} >
      {!rive && <img className="kumka-fallback" src={`${import.meta.env.BASE_URL}kumka.png`} alt="" />}
      <RiveComponent className="kumka-canvas" aria-hidden="true" />
    </div>
  );
}
